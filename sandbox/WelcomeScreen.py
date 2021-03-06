#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, Canvas, Text, Label, Button
from Tkinter import FLAT, RAISED
import tkFont

from StartPopupWindow import StartPopupWindow

DIM_X = 1200
DIM_Y = 900
BUTTON_PAD_X = 50
NUM_CHARS = 80
NUM_ROWS = 19

#---------------------------------------------------------------------#
# The WelcomeScreen is the first window shown to the user when GLIDE  #
# is started up. It contains the GLIDE logo and several buttons:      #
# "Play Game!" brings the user to the StartPopupWindow; "Getting      #
# Started" brings the user to an initial help screen; "About" brings  #
# the user to about details; and "Quit" exits.                        #
#---------------------------------------------------------------------#

class WelcomeScreen(Frame):

    def __init__(self, parent, mw):
        Frame.__init__(self, parent)
        parent.configure(bg="MediumTurquoise")
        self.parent = parent
        self.mw = mw

        # change font size depending on screen dimension
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # projector setting
        if screen_width == 1280:
	    self.customFont1 = tkFont.Font(family="LMMono10", size=20)
	    self.customFont = tkFont.Font(family="Pupcat", size=20, weight=tkFont.BOLD)
	    self.customFont2 = tkFont.Font(family="LMMono10", size=14)

	# single screen setting
	elif screen_width == 1920:
	    self.customFont1 = tkFont.Font(family="LMMono10", size=18)
	    self.customFont = tkFont.Font(family="Pupcat", size=16, weight=tkFont.BOLD)
            self.customFont2 = tkFont.Font(family="LMMono10", size=14)
            
	# double screen setting
	else:
            self.customFont1 = tkFont.Font(family="LMMono10", size=18)
            self.customFont = tkFont.Font(family="Pupcat", size=16, weight=tkFont.BOLD)
            self.customFont2 = tkFont.Font(family="LMMono10", size=14)

        self.initLogo()
        self.initToolbar()
        self.initScreen()

    def initLogo(self):
        self.topFrame = Frame(self.parent, relief=FLAT, background="MediumTurquoise")
        img = Image.open("./Graphics/logo.png")
        logoImg = ImageTk.PhotoImage(img)

        # make the logo the current item held in the topFrame
        self.currItem = Label(self.topFrame, relief=FLAT, background="MediumTurquoise", image=logoImg)
        self.currItem.image = logoImg
        self.currItem.pack()
        self.topFrame.grid(row=0)

    def initToolbar(self):
        toolbar = Frame(self.parent, relief=FLAT, background="MediumTurquoise")

        playButton = Button(toolbar, text="Play Game!", relief=RAISED, bg="Turquoise", activebackground="yellow",
                            font=self.customFont, command=self.openStartWindow)
        playButton.grid(row=0, column=0, padx=BUTTON_PAD_X)

        helpButton = Button(toolbar, text="Getting Started", relief=RAISED, bg="Turquoise", activebackground="yellow",
                            font=self.customFont, command=self.openGettingStartedWindow)
        helpButton.grid(row=0, column=1, padx=BUTTON_PAD_X)

        aboutButton = Button(toolbar, text="About", relief=RAISED, bg="Turquoise", activebackground="yellow",
                             font=self.customFont, command=self.openAboutWindow)
        aboutButton.grid(row=0, column=2, padx=BUTTON_PAD_X)

        quitButton = Button(toolbar, text="Quit", relief=RAISED, bg="Turquoise", activebackground="yellow",
                            font=self.customFont, command=self.onExit)
        quitButton.grid(row=0, column=3, padx=BUTTON_PAD_X)

        toolbar.grid(row=1)


    def initScreen(self):
        self.parent.grid_columnconfigure(0, minsize=DIM_X)
        self.parent.grid_rowconfigure(0, minsize=740)
        self.parent.grid_propagate(False)
        self.parent.resizable(width=False, height=False)


    # make the about text box the current item held in the topFrame
    def initAboutBox(self):
        file = open("../support/help/about", "r")
        gttext = file.read()
        self.currItem = Label(self.topFrame, bg="MediumTurquoise", relief=FLAT, font=self.customFont1,
                        width=NUM_CHARS, height=NUM_ROWS, text=gttext)
        self.currItem.pack()
        self.topFrame.grid(row=0)


    # make the getting started text box the current item held in the topFrame
    def initGettingStartedBox(self):
        file = open("../support/help/gettingstarted", "r")
        abouttext = file.read()
        self.currItem = Label(self.topFrame, bg="MediumTurquoise", relief=FLAT, font=self.customFont2,
                        width=NUM_CHARS, height=NUM_ROWS+7, 
                        text=abouttext)
        self.currItem.grid(row=0, column=0)
        self.topFrame.grid(row=0)


    def openStartWindow(self):
        frame = Frame(bg="")
        frame.pack()
        popup = StartPopupWindow(self)


    def openGettingStartedWindow(self):
        # first, destroy the current item held in the topFrame
        self.currItem.destroy()

        # then, make a new getting started box in the topFrame
        self.initGettingStartedBox()


    def openAboutWindow(self):
        # first, destroy the current item held in the topFrame
        self.currItem.destroy()

        # then, make a new about box in the topFrame
        self.initAboutBox()


    def onExit(self):
        self.parent.destroy()


    def createEnvt(self, username):
        self.mw.createNewEnvt(username)


def main():
    root = Tk()
    app = WelcomeScreen(root)
    root.mainloop()


if __name__ == '__main__':
    main()
