"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

from launcher.globals import LauncherGlobals

class SwitchLauncher():

	def __init__(self):
		self.gui = None
		self.injector = None

		print("Switch Launcher now running. Version: %s" % LauncherGlobals.CURR_VERSION)