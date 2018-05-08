"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

import sys

# First things first, are we using Python 3?
if sys.version_info < (3,0,0):
	print("Error: You need Python 3.0 or later to run Switch Launcher!")
	exit(1)

# Import dependencies. 
try:
	import usb
except ImportError as error:
	print(error)
	print("Error: One or more dependency is missing. Dependencies can be found in requirements.txt")
	exit(1)

# Start the show.
from launcher.core.SwitchLauncher import SwitchLauncher
base = SwitchLauncher()