"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

from launcher.globals import InjectorGlobals

class IWindowsInjector():

	def __init__(self, parent):
		print("Running with interface IWindowsInjector")

		self.parent = parent

	def triggerVulnerability(self, length):
		"""
		Currently, Windows injection is still a WIP.
		Stay tuned. For now, use Linux or MacOS.
		"""
		print("Triggering vulnerability...")
		return