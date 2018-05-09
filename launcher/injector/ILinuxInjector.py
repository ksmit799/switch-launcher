"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

import os
import ctypes
from glob import glob
from launcher.globals import InjectorGlobals

class SubmitURBIoctl(ctypes.Structure):
		_fields_ = [
			('type',          ctypes.c_ubyte),
			('endpoint',      ctypes.c_ubyte),
			('status',        ctypes.c_int),
			('flags',         ctypes.c_uint),
			('buffer',        ctypes.c_void_p),
			('buffer_length', ctypes.c_int),
			('actual_length', ctypes.c_int),
			('start_frame',   ctypes.c_int),
			('stream_id',     ctypes.c_uint),
			('error_count',   ctypes.c_int),
			('signr',         ctypes.c_uint),
			('usercontext',   ctypes.c_void_p),
		]

class ILinuxInjector():
	"""
	More complex vulnerability trigger for Linux as we can't go through pyusb
	as it limits control requests to a single page size, the limitation expressed
	by the usbfs. More realistically, the usbfs seems fine with it, and we just
	need to work around pyusb.
	"""

	SUPPORTED_USB_CONTROLLERS = ['pci/drivers/xhci_hcd', 'platform/drivers/dwc_otg']
	SETUP_PACKET_SIZE = 8
	URB_CONTROL_REQUEST = 2

	IOCTL_IOR = 0x80000000
	IOCTL_TYPE = ord('U')
	IOCTL_NR_SUBMIT_URB = 10

	def __init__(self, parent):
		print("Running with interface ILinuxInjector")

		self.parent = parent

		# Breaks Windows if we import at runtime.
		# Not apart of the Windows std library.
		import fcntl

		# We have some Linux specific warnings to print.
		print("IMPORTANT: On desktop Linux systems, we currently require an XHCI host controller.")
		print("A good way to ensure you're likely using an XHCI backend is to plug your switch into a blue 'USB 3' port.")
		print("If your switch isn't plugged into a USB 3 port, now is a good time to do so.")

	def triggerVulnerability(self, length):
		"""
		Submit the control request directly using the USBFS submit_urb
		ioctl, which issues the control request directly. This allows us
		to send our giant control request despite size limitations.
		"""

		# We only work for devices that are bound to a compatible HCD.
		isValid = self.validateEnvironment()
		if not isValid:
			print("error: The switch needs to be on an XHCI backend. Usually that means plugged into a blue USB 3.0 port!")
			return

		# Figure out the USB device file we're going to use to issue the control request.
		fd = os.open('/dev/bus/usb/{:0>3d}/{:0>3d}'.format(self.parent.usbDevice.bus, self.parent.usbDevice.address), os.O_RDWR)

		# Define the setup packet to be submitted.
		setupPacket = \
			int.to_bytes(InjectorGlobals.STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT, 1, byteorder='little') + \
			int.to_bytes(InjectorGlobals.GET_STATUS,                                  1, byteorder='little') + \
			int.to_bytes(0,                                                           2, byteorder='little') + \
			int.to_bytes(0,                                                           2, byteorder='little') + \
			int.to_bytes(length,                                                      2, byteorder='little')

		# Create a buffer to hold the result.
		bufferSize = self.SETUP_PACKET_SIZE + length
		buffer = ctypes.create_string_buffer(setupPacket, bufferSize)

		# Define the data structure used to issue the control request URB.
		request = SubmitURBIoctl()
		request.type = self.URB_CONTROL_REQUEST
		request.endpoint = 0
		request.buffer = ctypes.addressof(buffer)
		request.buffer_length = bufferSize

		# Manually submit an URB to the kernel, so it issues our 'evil' control request.
		ioctlNumber = (self.IOCTL_IOR | ctypes.sizeof(request) << 16 | self.IOCTL_TYPE << 8 | self.IOCTL_NR_SUBMIT_URB)
		fcntl.ioctl(fd, ioctlNumber, request, True)

		# Close our newly created fd.
		os.close(fd)

		# The other modules raise an IOError when the control request fails to complete. We don't fail out (as we don't bother
		# reading back), so we'll simulate the same behavior as the others.
		raise IOError("Raising an error to match the others!")

	def readNumFile(self, path):
		"""
		Reads a numeric value from a sysfs file that contains only a number.
		"""
		with open(path, 'r') as f:
			raw = f.read()
			return int(raw)

	def nodeMatchesOurDevice(self, path):
		"""
		Checks to see if the given sysfs node matches our given device.
		Can be used to check if an xhci_hcd controller subnode reflects a given device.
		"""

		# If this isn't a valid USB device node, it's not what we're looking for.
		if not os.path.isfile(path + "/busnum"):
			return False

		# We assume that a whole _bus_ is associated with a host controller driver, so we
		# only check for a matching bus ID.
		if self.parent.usbDevice.bus != self.readNumFile(path + "/busnum"):
			return False

		# If all of our checks passed, this is our device.
		return True

	def validateEnvironment(self):
		"""
		We can only inject giant control requests on devices that are backed
		by certain usb controllers. Typically, the xhci_hcd on most PCs.
		"""

		# Search each device bound to the xhci_hcd driver for the active device.
		for hciName in self.SUPPORTED_USB_CONTROLLERS:
			for path in glob("/sys/bus/{}/*/usb*".format(hciName)):
				if self.nodeMatchesOurDevice(path):
					return True

		return False