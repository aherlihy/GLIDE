#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, Button, Canvas, Text, PanedWindow, Scrollbar
from Tkinter import TOP, FLAT, RAISED, BOTH, X, Y, WORD, DISABLED, NORMAL, E, W, END, VERTICAL, RIGHT, LEFT
from Painter import Painter
import tkFont
import re
import sys
sys.path.append('/home/ecacciat/course/cs032/GLIDE/sandbox')
from tilemap import *

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
        self.levelFilename = "/home/ecacciat/course/cs032/GLIDE/support/levels/level"
        self.canRun = False

        self.initToolbar()
        self.initCanvas()
        self.initTextBoxes()
        self.initUI()
        self.initLevel(3)


    def initUI(self):
        self.parent.title("GLIDE")
        self.pack(fill=BOTH, expand=1)
        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))


    def initLevel(self, levelNum):
	name = self.levelFilename + str(levelNum)
	self.tilemap = TileMap(name)
	
	f = open(name, 'r')
	levelMap = []
	while True:
	    line = f.readline()
	    if line == '':
		break
	    levelMap.append(line)
	f.close()
	
	self.painter = Painter(self.canvas, levelMap)

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
        self.runButton = Button(toolbar, image=runImg, relief=FLAT, background="Turquoise", state=DISABLED,
                                activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.run)
        self.runButton.image = runImg
        self.runButton.grid(row=0, column=3)

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


    def initTextBoxes(self):
        panedWindow = PanedWindow(self.parent, width=DIM_X, height=(DIM_Y - TOOLBAR_Y)/2+5, relief=FLAT)
        self.customFont2 = tkFont.Font(family="LMMono10", size=14)


	# left-hand side: text box for the user to type into, plus a scrollbar
        leftPanel = Frame(panedWindow)
        scrollbar = Scrollbar(leftPanel, orient=VERTICAL)
        self.textEditor = Text(leftPanel, background="PaleTurquoise", width=MAX_CHARS, font=self.customFont2,
                               wrap=WORD, height=(DIM_Y - TOOLBAR_Y)/2, yscrollcommand=scrollbar.set)
        self.textEditor.bind("<<Modified>>", self.textEditorModified)
        self.resettingModifiedFlag = False

        # read in text from userTextFile.txt to put into the text editor
        f = open("userTextFile.txt", 'r')
        lineNum = 0
	while True:
	    line = f.readline()
	    if line == "":
		break
	    else:
		self.textEditor.insert(END, line)
	f.close()
	
	# add a scrollbar to the left-hand box
	scrollbar.config(command=self.textEditor.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textEditor.pack(side=LEFT, fill=BOTH, expand=1)
        panedWindow.add(leftPanel)


	# right hand side: help box, plus buttons to see different help screens
	customFont = tkFont.Font(family="Pupcat", size=14, weight=tkFont.BOLD)
	rightPanel = Frame(panedWindow)
	boxPanel = Frame(rightPanel, width=DIM_Y/2, height=DIM_X - 2*TOOLBAR_Y)
        self.helpBox = Text(boxPanel, background="LemonChiffon", font=self.customFont2,
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
        self.helpBox.pack(expand=1)
        boxPanel.pack()
        
        # set box panel's size so it doesn't resize


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

    def clearModifiedFlag(self):
	self.resettingModifiedFlag = True
	self.textEditor.edit_modified(False)
	self.resettingModifiedFlag = False


    def textEditorModified(self, selfCall=False, event=None):
	if self.resettingModifiedFlag == True:
	    return
	self.canRun = False
	self.runButton.config(state=DISABLED)
	self.clearModifiedFlag()


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

    # Save the user's code in the text editor into a file and tell the tilemap to check the code.
    def checkCode(self):
        f = open("userTextFile.txt", 'w')
        text = self.textEditor.get(1.0, END)
        f.write(text)
        f.close()

        error = self.tilemap.runLevelDummy("../GUI/userTextFile.txt")
        #error = False

        if error:
	    # read in the error file
	    errText = ""
	    f = open("../sandbox/output.py", 'r')
	    while True:
		line = f.readline()
		if line == "":
		    break
		else:
		    errText += line
	    f.close()

            # set the error text in the self.screens variable
            self.screens[-1] = errText
            self.runButton.config(state=DISABLED)

        else:
	    self.screens[-1] = "Yay! No compile or runtime errors!"
	    self.runButton.config(state=NORMAL)
	    self.canRun = True

	# show the new text in the "your code" part of the help box
	self.helpBox.config(state=NORMAL)   # turn on editing
	self.shownScreen = len(self.screens)-1
	self.helpBox.delete(1.0, END)   # clear text box
	self.helpBox.insert(END, self.screens[self.shownScreen])
	self.helpBox.config(state=DISABLED)   # turn off editing


    # Get the list of commands to execute from the tilemap and tell the painter to do them. This
    # allows us to look ahead for turns so we can animate them nicely.
    def run(self):
	
	if self.canRun:

	    cmdList = self.tilemap.getLevel()
	    #cmdList = "043350000005140043500"
	    
	    cmdList = re.sub('04350', 'i', cmdList) # i = s-bend east south
	    cmdList = re.sub('05140', 'j', cmdList) # j = s-bend east north
	    cmdList = re.sub('14051', 'k', cmdList) # k = s-bend north east
	    cmdList = re.sub('15241', 'l', cmdList) # l = s-bend north west
	    cmdList = re.sub('24152', 'm', cmdList) # m = s-bend west north
	    cmdList = re.sub('25342', 'n', cmdList) # n = s-bend west south
	    cmdList = re.sub('34253', 'o', cmdList) # o = s-bend south west
	    cmdList = re.sub('35043', 'p', cmdList) # p = s-bend south east
	    
	    cmdList = re.sub('043', 'a', cmdList)   # a = right turn south
	    cmdList = re.sub('051', 'b', cmdList)   # b = left turn north
	    cmdList = re.sub('342', 'c', cmdList)   # c = right turn west
	    cmdList = re.sub('350', 'd', cmdList)   # d = left turn east
	    cmdList = re.sub('253', 'e', cmdList)   # e = left turn south
	    cmdList = re.sub('241', 'f', cmdList)   # f = right turn north
	    cmdList = re.sub('152', 'g', cmdList)   # g = left turn west
	    cmdList = re.sub('140', 'h', cmdList)   # h = right turn east

	    for i in range(len(cmdList)):
		cmd = cmdList[i]
		if cmd == '0':
		    self.painter.movePlaneEast()
		elif cmd == '1':
		    self.painter.movePlaneNorth()
		elif cmd == '2':
		    self.painter.movePlaneWest()
		elif cmd == '3':
		    self.painter.movePlaneSouth()
		elif cmd == '4':
		    self.painter.rotatePlaneClockwise(90)
		elif cmd == '5':
		    self.painter.rotatePlaneCounterclockwise(90)
		elif cmd == '6':
		    pass
		elif cmd == '7':
		    pass
		elif cmd == 'a':
		    self.painter.takeRightTurnSouth()
		elif cmd == 'b':
		    self.painter.takeLeftTurnNorth()
		elif cmd == 'c':
		    self.painter.takeRightTurnWest()
		elif cmd == 'd':
		    self.painter.takeLeftTurnEast()
		elif cmd == 'e':
		    self.painter.takeLeftTurnSouth()
		elif cmd == 'f':
		    self.painter.takeRightTurnNorth()
		elif cmd == 'g':
		    self.painter.takeLeftTurnWest()
		elif cmd == 'h':
		    self.painter.takeRightTurnEast()
		elif cmd == 'i':
		    self.painter.sBendEastSouth()
		elif cmd == 'j':
		    self.painter.sBendEastNorth()
		elif cmd == 'k':
		    self.painter.sBendNorthEast()
		elif cmd == 'l':
		    self.painter.sBendNorthWest()
		elif cmd == 'm':
		    self.painter.sBendWestNorth()
		elif cmd == 'n':
		    self.painter.sBendWestSouth()
		elif cmd == 'o':
		    self.painter.sBendSouthWest()
		elif cmd == 'p':
		    self.painter.sBendSouthEast()
		else:
		    print ("Unknown movement command %i; not executing." % cmd)

	    # check for a win, or an "inefficient" win - reached goal but had extra cmds at end
	    match = re.search('7', cmdList)
	    if match != None and match.start() == length(cmdList)-1:    # actual win
		self.screens[-1] = "Congrats! You beat the level!\n\nYou can hit the Next Level button to" \
				    "move on, or try out other cool stuff with your plane here."
	    elif match != None:    # inefficient win
		self.screens[-1] = "You reached the goal, but your code contained some extra stuff -" \
				    "try making your plane reach the goal in as few lines of code as possible."
	    else:      # didn't hit goal at all
		self.screens[-1] = "Oops! Your plane didn't make it to the goal."

	    # show the new text in the "your code" part of the help box
	    self.helpBox.config(state=NORMAL)   # turn on editing
	    self.shownScreen = len(self.screens)-1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
	    self.helpBox.config(state=DISABLED)   # turn off editing


def main():
    root = Tk()
    app = Environment(root)
    root.mainloop()


if __name__ == '__main__':
    main()