"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

from launcher.injector.PayloadInjector import PayloadInjector
from launcher.gui.LauncherGUI import LauncherGUI
from launcher.globals import LauncherGlobals

class SwitchLauncher():

	def __init__(self):
		self.injector = PayloadInjector(self)
		self.gui = LauncherGUI(self)

		print("Switch Launcher now running. Version: %s" % LauncherGlobals.CURR_VERSION)

	def shutdown(self):
		print("Shutting down...")
		self.injector.shutdown()
		self.gui.shutdown()
		exit(0)