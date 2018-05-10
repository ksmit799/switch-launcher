"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

"""
We could just hard code strings into the GUI.
However, with the possibility of translation
to other languages in the future, we stick all
strings into this file.
"""

WINDOW_TITLE = "Switch Launcher [%s]"

VAR_NOT_SET = "None"

DEVICE_ID = "Device ID: %s"
INTERMEZZO = "Selected Intermezzo: %s"
PAYLOAD = "Selected Payload: %s"
START = "Connect and Inject"

CHOOSE_INTERMEZZO = "Choose Intermezzo"
CHOOSE_PAYLOAD = "Choose Payload"

POPUP_ERROR = {
	'VarsNotSet': "You must select both an Intermezzo bin file and a Payload bin file.",
	'NoBackend': "You must install a native usb backend for your system. More info on the GitHub repository.",
	'UnableToLocate': "Unable to locate a connected Nintendo Switch. Try plugging it into a USB 3 port.",
	'PayloadTooBig': "Selected payload is too large to be submitted via RCM.",
	'UnknownError': "An unknown error occured while triggering the exploit. Please try again with possibly a different payload."
}

POPUP_INFO = {
	'SuccessfulExploit': "SUCCESS! The exploit has been triggered and you can now safely unplug your Switch!"
}