#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, Button, Canvas, Text, PanedWindow, Scrollbar
from Tkinter import TOP, FLAT, RAISED, BOTH, X, Y, WORD, DISABLED, NORMAL, E, W, END, VERTICAL, RIGHT, LEFT
from Painter import Painter
import tkFont

DIM_X = 1200
DIM_Y = 900
TOOLBAR_Y = 70
MAX_CHARS = 59
BUTTON_X = 155
BUTTON_Y = 32
SCREEN_BUTTON_X = 10
CANVAS_HEIGHT = (DIM_Y - TOOLBAR_Y)/2+25

#--------------------------------------------------------------------------#
# The Environment class is the screen where the user will play the game.   #
# It includes a canvas where objects will be drawn and animated, a re-     #
# sizable text editor window, and a resizable help box. At the top there   #
# is a toolbar with buttons to Save Level, Load Level, Load Profile,       #
# Check Code, and Play (run code). The user is brought to this screen      #
# after selecting a username from the StartPopupWindow.                    #
#--------------------------------------------------------------------------#

class Environment(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="MediumTurquoise")
        self.parent = parent
        self.initToolbar()
        self.initCanvas()
        self.initTextBoxes()
        self.initUI()

    def initUI(self):
        self.parent.title("GLIDE")
        self.pack(fill=BOTH, expand=1)
        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))

    def initToolbar(self):
        toolbar = Frame(self.parent, relief=FLAT, background="MediumTurquoise")

        img = Image.open("Graphics/Icons/saveIcon.png")
        saveImg1 = ImageTk.PhotoImage(img)  
        saveLevelButton = Button(toolbar, image=saveImg1, relief=FLAT, background="Turquoise",
                                 activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.save)
        saveLevelButton.image = saveImg1
        saveLevelButton.grid(row=0, column=0)

        img = Image.open("Graphics/Icons/loadIcon.png")
        runImg = ImageTk.PhotoImage(img)  
        runButton = Button(toolbar, image=runImg, relief=FLAT, background="Turquoise",
                           activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.load)
        runButton.image = runImg
        runButton.grid(row=0, column=1)

        img = Image.open("Graphics/Icons/checkIcon.png")
        checkImg = ImageTk.PhotoImage(img)  
        checkButton = Button(toolbar, image=checkImg, relief=FLAT, background="Turquoise",
                             activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.checkCode)
        checkButton.image = checkImg
        checkButton.grid(row=0, column=2)

        img = Image.open("Graphics/Icons/runIcon.png")
        runImg = ImageTk.PhotoImage(img)  
        runButton = Button(toolbar, image=runImg, relief=FLAT, background="Turquoise",
                           activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.run)
        runButton.image = runImg
        runButton.grid(row=0, column=3)

        img = Image.open("Graphics/Icons/quitIcon.png")
        quitImg = ImageTk.PhotoImage(img)  
        quitButton = Button(toolbar, image=quitImg, relief=FLAT, background="Turquoise",
                            activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.exit)
        quitButton.image = quitImg
        quitButton.grid(row=0, column=4, sticky=E)

        toolbar.pack(side=TOP, fill=X)


    def initCanvas(self):
        self.canvas = Canvas(self.parent, width=DIM_X, height=CANVAS_HEIGHT, background="white", relief=FLAT)
        self.canvas.pack()

        # Test map:
        m = [['A']*25 for _ in range(10)]
        m[0][0] = 'W'
        m[0][1] = 'W'
        m[0][2] = 'W'    # test how all 3 horiz pieces fit together

        m[0][4] = 'W'
        m[0][5] = 'W'    # test how the 2 end horiz pieces fit
        
        m[2][0] = 'W'
        m[3][0] = 'W'
        m[4][0] = 'W'   # test how all 3 vertical pieces fit
        
        m[6][0] = 'W'
        m[7][0] = 'W'    # test how 2 end vertical pieces fit
        
        m[2][2] = 'W'
        m[2][3] = 'W'
        m[2][4] = 'W'
        m[2][5] = 'W'
        m[2][6] = 'W'
        m[3][2] = 'W'
        m[3][4] = 'W'
        m[3][6] = 'W'
        m[4][2] = 'W'
        m[4][3] = 'W'
        m[4][4] = 'W'
        m[4][5] = 'W'
        m[4][6] = 'W'
        m[5][2] = 'W'
        m[5][4] = 'W'
        m[5][6] = 'W'
        m[6][2] = 'W'
        m[6][3] = 'W'
        m[6][4] = 'W'
        m[6][5] = 'W'
        m[6][6] = 'W'    # test a little square

        m[9][9] = 'I'  # test an individual cloud
        
        m[3][10] = 'I'
        m[3][11] = 'I'
        m[3][12] = 'I'
        m[4][10] = 'I'
        m[4][11] = 'I'
        m[4][12] = 'I'
        m[5][10] = 'I'
        m[5][11] = 'I'
        m[5][12] = 'I'
        
        m[5][15] = 'G'
        
        m[5][20] = 'P'

        self.painter = Painter(self.canvas, m)


    def initTextBoxes(self):
        panedWindow = PanedWindow(self.parent, width=DIM_X, height=(DIM_Y - TOOLBAR_Y)/2+5, relief=FLAT)
        self.customFont2 = tkFont.Font(family="LMMono10", size=14)


	# left-hand side: text box for the user to type into, plus a scrollbar
        leftPanel = Frame(panedWindow)
        scrollbar = Scrollbar(leftPanel, orient=VERTICAL)
        textEditor = Text(leftPanel, background="PaleTurquoise", width=MAX_CHARS, font=self.customFont2,
                          wrap=WORD, height=(DIM_Y - TOOLBAR_Y)/2, yscrollcommand=scrollbar.set)

        # read in text from userTextFile.txt to put into the text editor
        f = open("userTextFile.txt", 'r')
        lineNum = 0
	while True:
	    line = f.readline()
	    if line == "":
		break
	    else:
		textEditor.insert(END, line)
	f.close()
	
	# add a scrollbar to the left-hand box
	scrollbar.config(command=textEditor.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        textEditor.pack(side=LEFT, fill=BOTH, expand=1)
        panedWindow.add(leftPanel)


	# right hand side: help box, plus buttons to see different help screens
	customFont = tkFont.Font(family="Pupcat", size=14, weight=tkFont.BOLD)
	rightPanel = Frame(panedWindow)
        self.helpBox = Text(rightPanel, background="LemonChiffon", width=MAX_CHARS, font=self.customFont2,
                            wrap=WORD, height=15)

        # read in text from helpTextFile.txt to put into the help box - what we want to show on each screen
        # is in its own string inside the "screens"
        f = open("helpTextFile.txt", 'r')
        self.screens = []
        self.screens.append("")
        numScreen = 0

	while True:
	    line = f.readline()
	    if line == "":
		break
	    elif line == "*****\n":
		self.screens.append("")
		numScreen += 1
	    else:
		self.screens[numScreen] += line
	f.close()
	
	# insert the first screen's text into the help box and set a variable saying so
	self.helpBox.insert(END, self.screens[0])
	self.shownScreen = 0
	
        self.helpBox.config(state=DISABLED)
        self.helpBox.pack()

	helpboxWidth = self.helpBox.winfo_reqwidth()
        buttonBar = Frame(rightPanel, relief=FLAT, background="LemonChiffon", height=BUTTON_Y, width=helpboxWidth)
        prevButton =     Button(buttonBar, relief=RAISED, background="LemonChiffon", text="Previous", borderwidth=1,
                                activebackground="Turquoise", width=SCREEN_BUTTON_X, height=BUTTON_Y, command=self.prevScreen,
                                font=customFont)
        yourCodeButton = Button(buttonBar, relief=RAISED, background="LemonChiffon", text="Your Code", borderwidth=1,
                                activebackground="Turquoise", width=SCREEN_BUTTON_X, height=BUTTON_Y, command=self.lastScreen,
                                font=customFont)
        nextButton =     Button(buttonBar, relief=RAISED, background="LemonChiffon", text="Next", borderwidth=1,
                                activebackground="Turquoise", width=SCREEN_BUTTON_X, height=BUTTON_Y, command=self.nextScreen,
                                font=customFont)
	prevButton.pack(side=LEFT)
	yourCodeButton.pack(side=LEFT, padx=103)
	nextButton.pack(side=LEFT)
	buttonBar.pack(anchor=W)
	
        panedWindow.add(rightPanel)
        panedWindow.pack(fill=BOTH, expand=1)

    def prevScreen(self):
	if self.shownScreen == 0:
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # first, turn on editing
	    self.shownScreen -= 1
	    self.helpBox.delete(1.0, END)   # clear the text box first
	    self.helpBox.insert(END, self.screens[self.shownScreen])   # add the prev screen's text
	    self.helpBox.config(state=DISABLED)  # turn off editing again
    
    def lastScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # turn on editing
	    self.shownScreen = len(self.screens)-1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
            self.helpBox.config(state=DISABLED)   # turn off editing
    
    def nextScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # first, turn on editing
	    self.shownScreen += 1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
            self.helpBox.config(state=DISABLED)   # turn off editing

    def exit(self):
        self.quit()

    def save(self):
        pass

    def load(self):
        pass

    def checkCode(self):
        pass

    def run(self):
	
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.takeRightTurnSouth()
	self.painter.movePlaneSouth()
	self.painter.movePlaneSouth()
	self.painter.movePlaneSouth()
	self.painter.takeLeftTurnEast()
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.movePlaneEast()
	self.painter.takeLeftTurnNorth()
	self.painter.movePlaneNorth()
	self.painter.movePlaneNorth()
	self.painter.movePlaneNorth()
	self.painter.takeLeftTurnWest()
	for i in range(8):
	    self.painter.movePlaneWest()
	



def main():
    root = Tk()
    app = Environment(root)
    root.mainloop()


if __name__ == '__main__':
    main()