"""
 * Written by the Trapdoor-NX team, May 8, 2018.
 * Licensing information can found in the 'LICENSE' file.
 * Injector based on reswitched/fusee-launcher.
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from launcher.globals import GUIGlobals
from launcher.globals import LauncherGlobals

class LauncherGUI(tk.Tk):

	def __init__(self, parent):
		self.parent = parent
		self.tk = None

	def shutdown(self):
		if self.tk is not None:
			self.tk.quit()

	def quitCallback(self):
		self.parent.shutdown()

	def run(self):
		super().__init__()

		self.protocol("WM_DELETE_WINDOW", self.quitCallback)

		self.title(GUIGlobals.WINDOW_TITLE % LauncherGlobals.CURR_VERSION)
		self.geometry("500x300")

		# Create our ttk styles.
		# ttk allows us to use the systems native UI.
		style = ttk.Style()
		style.configure("TLabel", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
		style.configure("B.TLabel", font=(None, 40))
		style.configure("B.TButton", foreground="black", background="lightgrey", font=(None, 16), anchor="center")
		style.configure("TEntry", foregound="black", background="white")

		# Create our main frame.
		self.mainFrame = tk.Frame(self, width=500, height=300, bg="lightgrey")

		# General information to be filled out by the injector.

		# Device ID var.
		self.deviceIDVar = tk.StringVar(self.mainFrame)
		self.deviceIDVar.set(GUIGlobals.DEVICE_ID % GUIGlobals.VAR_NOT_SET)

		# Device ID label.
		self.deviceIdLabel = ttk.Label(self.mainFrame, textvar=self.deviceIDVar)

		# Intermezzo path var.
		# THIS IS THE GUI DISPLAYED VERSION. DO NOT USE THIS AS THE PATH VAR.
		self.intermezzoPathVar = tk.StringVar(self.mainFrame)
		self.intermezzoPathVar.set(GUIGlobals.INTERMEZZO % GUIGlobals.VAR_NOT_SET)

		# Intermezzo path label.
		self.intermezzoPathLabel = ttk.Label(self.mainFrame, textvar=self.intermezzoPathVar)

		# Payload path var.
		# THIS IS THE GUI DISPLAYED VERSION. DO NOT USE THIS AS THE PATH VAR.
		self.payloadPathVar = tk.StringVar(self.mainFrame)
		self.payloadPathVar.set(GUIGlobals.PAYLOAD % GUIGlobals.VAR_NOT_SET)

		# Payload path label.
		self.payloadPathLabel = ttk.Label(self.mainFrame, textvar=self.payloadPathVar)

		# The Intermezzo path button.
		self.intermezzoButton = ttk.Button(self.mainFrame, text=GUIGlobals.CHOOSE_INTERMEZZO, command=self.openIntermezzoSelector, style="B.TButton")

		# The Payload path button.
		self.payloadButton = ttk.Button(self.mainFrame, text=GUIGlobals.CHOOSE_PAYLOAD, command=self.openPayloadSelector, style="B.TButton")

		# The start button.
		self.startButton = ttk.Button(self.mainFrame, text=GUIGlobals.START, command=None, style="B.TButton")
		
		self.mainFrame.pack(fill=tk.BOTH, expand=1)

		# Pack labels.
		self.deviceIdLabel.pack(fill=tk.X, pady=15)
		self.intermezzoPathLabel.pack(fill=tk.X, pady=15)
		self.payloadPathLabel.pack(fill=tk.X, pady=15)

		# Pack buttons.
		self.intermezzoButton.pack(fill=tk.X, padx=50)
		self.payloadButton.pack(fill=tk.X, padx=50)
		self.startButton.pack(fill=tk.X, padx=50)

		self.mainloop()

	def blockInput(self):
		pass

	def returnInput(self):
		pass

	def openIntermezzoSelector(self):
		# Block button input.
		self.blockInput()

		# Open a new file explorer to locate the file.
		filePath = askopenfilename()

		# If they didn't choose a file, do nothing.
		if filePath == '':
			self.returnInput()
			return

		# Get the selected filename and extension.
		fileName, fileExtension = os.path.splitext(filePath)

		# Make sure they have selected a valid bin file.
		if fileExtension != '.bin':
			# TODO: Popup error message.
			print("Invalid file selected when browsing for Intermezzo. It should have a .bin extension!")
			self.returnInput()
			return

		# They've selected a valid bin file. Update our vars.
		self.intermezzoPathVar.set(GUIGlobals.INTERMEZZO % os.path.basename(filePath))

		print(fileName)

	def openPayloadSelector(self):
		# Block button input.
		self.blockInput()

		# Open a new file explorer to locate the file.
		filePath = askopenfilename()

		# If they didn't choose a file, do nothing.
		if filePath == '':
			self.returnInput()
			return

		# Get the selected filename and extension.
		fileName, fileExtension = os.path.splitext(filePath)

		# Make sure they have selected a valid bin file.
		if fileExtension != '.bin':
			# TODO: Popup error message.
			print("Invalid file selected when browsing for Payload. It should have a .bin extension!")
			self.returnInput()
			return

		# They've selected a valid bin file. Update our vars.
		self.payloadPathVar.set(GUIGlobals.PAYLOAD % os.path.basename(filePath))

		print(fileName)