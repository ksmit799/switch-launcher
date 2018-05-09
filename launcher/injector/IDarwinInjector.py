"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

from launcher.globals import InjectorGlobals

class IDarwinInjector():

	def __init__(self, parent):
		print("Running with interface IDarwinInjector")

		self.parent = parent

	def triggerVulnerability(self, length):
		"""
		Triggering the vulnerability is simplest on macOS; we simply issue the control request as-is.
		"""
		print("Triggering vulnerability...")

		return self.parent.usbDevice.ctrl_transfer(InjectorGlobals.STANDARD_REQUEST_DEVICE_TO_HOST_TO_ENDPOINT, InjectorGlobals.GET_STATUS, 0, 0, length)