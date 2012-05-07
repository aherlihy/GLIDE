#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, BOTH, Canvas, Text, PanedWindow
from Tkinter import Button, LEFT, TOP, X, FLAT, RAISED, BOTH
from WelcomeScreen import WelcomeScreen
from Environment import Environment
=======
from GlideChoose import GlideChoose

DIM_X = 1200
DIM_Y = 900

#-----------------------------------------------------------------------#
# The MainWindow is the frame that holds all of the other windows that  #
# the GLIDE program uses. It has no functionality other than being a    #
# container for other frames and hiding/showing things when necessary.  #
#-----------------------------------------------------------------------#

class MainWindow(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("GLIDE")
        self.welcomeScreen = WelcomeScreen(self.parent, self)  # can create a StartPopupWindow

        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))
        self.pack()

        self.envt = None
        self.parent.protocol("WM_DELETE_WINDOW", self.exit)

    def createNewEnvt(self, username):
	self.welcomeScreen.pack_forget()
        self.envt = Environment(self.parent, username)
        self.envt.pack()

    def exit(self):
	frame = Frame(bg="")
        frame.pack()
        popup = GlideChoose(self, "Are you sure you want to quit?", "Quit GLIDE", True)


    def kill(self):
	#if self.envt != None:
	#    self.envt.painter.destroy()
	#    self.envt.destroy()
	self.parent.destroy()

def main():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
