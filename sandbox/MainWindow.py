#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, BOTH, Canvas, Text, PanedWindow
from Tkinter import Button, LEFT, TOP, X, FLAT, RAISED, BOTH
from WelcomeScreen import WelcomeScreen
from Environment import Environment

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
        welcomeScreen = WelcomeScreen(self.parent, self)  # can create a StartPopupWindow

        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))
        self.pack()

    def createNewEnvt(self):
        envt = Environment(self.parent)
        self.pack()

def main():
    root = Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()