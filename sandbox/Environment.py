#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, Button, Canvas, Text, PanedWindow, Scrollbar
from Tkinter import TOP, FLAT, RAISED, BOTH, X, Y, WORD, DISABLED, NORMAL, E, W, END, VERTICAL, RIGHT, LEFT
from Painter import Painter
import tkFont
import re
from tilemap import *

import time

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
        self.levelFilename = "../support/levels/level"
        self.stencilFilename = "../support/stencil/level"
        self.helpFilename = "../support/help/level"
        self.canRun = False

        self.initToolbar()
        self.initCanvas()
        self.initTextBoxes()
        self.initUI()
        
        self.currLevel = 1
        self.beatenLevels = []
        self.initLevel(self.currLevel)


    def initUI(self):
        self.parent.title("GLIDE")
        self.pack(fill=BOTH, expand=1)
        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))


    def initLevel(self, levelNum):
	
	# create the canvas
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
	
	# clear the text editor
	self.textEditor.delete(1.0, END)
	
	# put stencil code into the text editor
	name = self.stencilFilename + str(levelNum)
        f = open(name, 'r')
        lineNum = 0
	while True:
	    line = f.readline()
	    if line == "":
		break
	    else:
		self.textEditor.insert(END, line)
	f.close()
	
	# allow editing for the help box and clear it
	self.helpBox.config(state=NORMAL)
	self.helpBox.delete(1.0, END)   # clear text boxes
	
	# put help files into the help box - what we want to show on each screen
        # is in its own string inside the "screens"
        name = self.helpFilename + str(levelNum)
        f = open(name, 'r')
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
	
	# disable editing again
        self.helpBox.config(state=DISABLED)


    def initToolbar(self):
        toolbar = Frame(self.parent, relief=FLAT, background="MediumTurquoise")

        img = Image.open("Graphics/Icons/saveIcon.png")
        saveImg1 = ImageTk.PhotoImage(img)  
        self.saveLevelButton = Button(toolbar, image=saveImg1, relief=FLAT, background="Turquoise",
                                      activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.save)
        self.saveLevelButton.image = saveImg1
        self.saveLevelButton.grid(row=0, column=0)

        img = Image.open("Graphics/Icons/loadIcon.png")
        loadImg = ImageTk.PhotoImage(img)  
        self.loadButton = Button(toolbar, image=loadImg, relief=FLAT, background="Turquoise",
                                 activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.load)
        self.loadButton.image = loadImg
        self.loadButton.grid(row=0, column=1)

        img = Image.open("Graphics/Icons/checkIcon.png")
        checkImg = ImageTk.PhotoImage(img)  
        self.checkButton = Button(toolbar, image=checkImg, relief=FLAT, background="Turquoise",
                                  activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.checkCode)
        self.checkButton.image = checkImg
        self.checkButton.grid(row=0, column=2)

        img = Image.open("Graphics/Icons/runIcon.png")
        runImg = ImageTk.PhotoImage(img)  
        self.runButton = Button(toolbar, image=runImg, relief=FLAT, background="Turquoise", state=DISABLED,
                                activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.run)
        self.runButton.image = runImg
        self.runButton.grid(row=0, column=3)

        img = Image.open("Graphics/Icons/prevLevelIcon.png")
        prevLevelImg = ImageTk.PhotoImage(img)  
        self.prevLevelButton = Button(toolbar, image=prevLevelImg, relief=FLAT, background="Turquoise", state=DISABLED,
                                 activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.prevLevel)
        self.prevLevelButton.image = prevLevelImg
        self.prevLevelButton.grid(row=0, column=4)

        img = Image.open("Graphics/Icons/nextLevelIcon.png")
        nextLevelImg = ImageTk.PhotoImage(img)  
        self.nextLevelButton = Button(toolbar, image=nextLevelImg, relief=FLAT, background="Turquoise", state=DISABLED,
                                 activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.nextLevel)
        self.nextLevelButton.image = nextLevelImg
        self.nextLevelButton.grid(row=0, column=5)

        img = Image.open("Graphics/Icons/quitIcon.png")
        quitImg = ImageTk.PhotoImage(img)  
        quitButton = Button(toolbar, image=quitImg, relief=FLAT, background="Turquoise",
                            activebackground="yellow", width=BUTTON_X, height=BUTTON_Y, command=self.exit)
        quitButton.image = quitImg
        quitButton.grid(row=0, column=7, sticky=E)

        toolbar.pack(side=TOP, fill=X)


    def disableButtons(self):
	currStates = [self.saveLevelButton.config().get('state')[4],
	              self.loadButton.config().get('state')[4],
	              self.checkButton.config().get('state')[4],
	              self.runButton.config().get('state')[4],
	              self.prevLevelButton.config().get('state')[4],
	              self.nextLevelButton.config().get('state')[4]]
	
	# set all to disabled
	self.saveLevelButton.config(state=DISABLED)
	self.loadButton.config(state=DISABLED)
	self.checkButton.config(state=DISABLED)
	self.runButton.config(state=DISABLED)
	self.prevLevelButton.config(state=DISABLED)
	self.nextLevelButton.config(state=DISABLED)
	
	return currStates
	
    def returnButtonsToStates(self, states):
	self.saveLevelButton.config(state=states[0])
	self.loadButton.config(state=states[1])
	self.checkButton.config(state=states[2])
	self.runButton.config(state=states[3])
	self.prevLevelButton.config(state=states[4])
	self.nextLevelButton.config(state=states[5])
	

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
        self.helpBox.pack(expand=1)
        boxPanel.pack()

        # add buttons to help box
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


    # deals with making the "run code" button appear grayed-out when the user modifies the
    # input box, so that you have to re-compile before running
    def clearModifiedFlag(self):
	self.resettingModifiedFlag = True
	self.textEditor.edit_modified(False)
	self.resettingModifiedFlag = False


    # same as above comment
    def textEditorModified(self, selfCall=False, event=None):
	if self.resettingModifiedFlag == True:
	    return
	self.canRun = False
	self.runButton.config(state=DISABLED)
	self.clearModifiedFlag()


    # Show the previous screen in the help box
    def prevScreen(self):
	if self.shownScreen == 0:
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # first, turn on editing
	    self.shownScreen -= 1
	    self.helpBox.delete(1.0, END)   # clear the text box first
	    self.helpBox.insert(END, self.screens[self.shownScreen])   # add the prev screen's text
	    self.helpBox.config(state=DISABLED)  # turn off editing again


    # Show the last ("Your Code") screen in the help box
    def lastScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # turn on editing
	    self.shownScreen = len(self.screens)-1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
            self.helpBox.config(state=DISABLED)   # turn off editing


    # Show the next screen in the help box
    def nextScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # first, turn on editing
	    self.shownScreen += 1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
            self.helpBox.config(state=DISABLED)   # turn off editing


    # Exit the GUI
    def exit(self):
	self.cleanUp()
        self.quit()

    def save(self):
        pass

    def load(self):
        pass

    # Save the user's code in the text editor into a file and tell the tilemap to check the code.
    def checkCode(self):
        f = open("code", 'w')
        text = self.textEditor.get(1.0, END)
        f.write(text)
        f.close()

        # disable buttons & show "checking" dialog while we run the level dummy
        currStates = self.disableButtons()
        self.painter.showCheckingText()
        self.update()

        # run the level dummy to see if the code compiles
        noError = self.tilemap.runLevelDummy("code")

        # return buttons to their states once the method has returned & hide "checking" dialog
        self.returnButtonsToStates(currStates)
        self.painter.hideCheckingText()

        if not noError:
	    # the error line to highlight in the code
	    errorLine = 0

	    # read in the error file
	    errText = ""
	    f = open("output.py", 'r')
	    while True:
		line = f.readline()
		if line == "":
		    break
		elif line.startswith("line"):
		    lineStuff = line.split(' ')
		    errorLine = int(lineStuff[1]) - 5
		    line = "line: " + str(errorLine) + "\n"
		    errText += line
		else:
		    errText += line
	    f.close()

            # set the error text in the self.screens variable
            self.screens[-1] = errText
            self.runButton.config(state=DISABLED)

        else:
	    # reset plane
	    self.painter.initPlane()
	    
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
	    
	    # make the run button un-clickable for the duration of the animation
	    #self.runButton.config(state=DISABLED)
	    # disable buttons while we run the level dummy
            currStates = self.disableButtons()
	    
	    # reset plane
	    self.painter.initPlane()

	    cmdList = self.tilemap.getLevel()
	    
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
		elif cmd == '6':     # crash
		    self.screens[-1] = "Oh no - your plane crashed!"
		    self.helpBox.config(state=NORMAL)   # turn on editing
	            self.shownScreen = len(self.screens)-1
	            self.helpBox.delete(1.0, END)   # clear text box
	            self.helpBox.insert(END, self.screens[self.shownScreen])
	            self.helpBox.config(state=DISABLED)   # turn off editing
	            return
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
	    if match != None and match.start() == len(cmdList)-1:    # actual win
		self.screens[-1] = "Congrats! You beat the level!\n\nYou can hit the Next Level button to" \
				    "move on, or try out other cool stuff with your plane here."
		self.beatenLevels.append(self.currLevel)
		currStates[5] = "normal"
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
	    
	    # make the run button clickable again
	    #self.runButton.config(state=NORMAL)
	    self.returnButtonsToStates(currStates)


    def prevLevel(self):
	self.currLevel -= 1
	self.initLevel(self.currLevel)
	
	# do the appropriate graying-out of buttons
	if self.currLevel == 1:
	    self.prevLevelButton.config(state=DISABLED)
	else:
	    self.prevLevelButton.config(state=NORMAL)
	self.nextLevelButton.config(state=NORMAL)
	self.runButton.config(state=DISABLED)


    def nextLevel(self):
	self.currLevel += 1
	self.initLevel(self.currLevel)
	
	# do the appropriate graying-out of buttons
	if self.currLevel in self.beatenLevels and self.currLevel < 3:
	    self.nextLevelButton.config(state=NORMAL)
	else:
	    self.nextLevelButton.config(state=DISABLED)
	self.prevLevelButton.config(state=NORMAL)
	self.runButton.config(state=DISABLED)


    def cleanUp(self):
	f = open("runLevel.py", "w")
	f.close()


def main():
    root = Tk()
    app = Environment(root)
    root.mainloop()


if __name__ == '__main__':
    main()