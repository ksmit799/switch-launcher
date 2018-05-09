"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

import threading
import tkinter

class LauncherGUI(threading.Thread):

	def __init__(self, parent):
		threading.Thread.__init__(self)

		self.parent = parent
		self.tk = None

		self.start()

	def shutdown(self):
		if self.tk is not None:
			self.tk.quit()

	def quitCallback(self):
		self.parent.shutdown()

	def run(self):
		self.tk = tkinter.Tk()
		self.tk.protocol("WM_DELETE_WINDOW", self.quitCallback)

		label = tkinter.Label(self.tk, text="Hello World")
		label.pack()

		self.tk.mainloop()