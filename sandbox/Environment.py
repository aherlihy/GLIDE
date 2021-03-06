#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Menu, Button, Canvas, Text, PanedWindow, Scrollbar
from Tkinter import TOP, FLAT, RAISED, BOTH, X, Y, WORD, DISABLED, NORMAL, E, W, END, VERTICAL, RIGHT, LEFT
from Painter import Painter
import tkFont, re, time
from tilemap import *
import maze

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

    def __init__(self, root, mw, username):
        Frame.__init__(self, root, background="MediumTurquoise")
        self.parent = root
        self.mw = mw
        self.username = username

        self.levelFilename = "../support/levels/level"
        self.stencilFilename = "../support/stencil/level"
        self.helpFilename = "../support/help/level"
        self.canRun = False
        self.endStatus = False

        # change font size depending on screen dimension
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # projector setting
        if screen_width == 1280:
	    self.customFont1 = tkFont.Font(family="Pupcat", size=18, weight=tkFont.BOLD)
	    self.customFont2 = tkFont.Font(family="LMMono10", size=17)
	    self.boldFont = tkFont.Font(family="LMMono10", size=17, weight=tkFont.BOLD)
	    self.italFont = tkFont.Font(family="LMMono10", size=17, slant=tkFont.ITALIC)

	# single screen setting
	elif screen_width == 1920:
	    self.customFont1 = tkFont.Font(family="Pupcat", size=14, weight=tkFont.BOLD)
	    self.customFont2 = tkFont.Font(family="LMMono10", size=14)
	    self.boldFont = tkFont.Font(family="LMMono10", size=14, weight=tkFont.BOLD)
	    self.italFont = tkFont.Font(family="LMMono10", size=14, slant=tkFont.ITALIC)

	# double screen setting
	else:
	    self.customFont1 = tkFont.Font(family="Pupcat", size=14, weight=tkFont.BOLD)
            self.customFont2 = tkFont.Font(family="LMMono10", size=15)
            self.boldFont = tkFont.Font(family="LMMono10", size=14, weight=tkFont.BOLD)
	    self.italFont = tkFont.Font(family="LMMono10", size=14, slant=tkFont.ITALIC)


        self.initToolbar()
        self.initCanvas()
        self.initTextBoxes()
        self.initUI()

        self.currLevel = 1

        self.beatenLevels = []
        self.initLevelCanvas()
        self.initLevelText()
        maze.create_maze()


    def initUI(self):
        self.parent.title("GLIDE")
        self.pack(fill=BOTH, expand=1)
        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.parent.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))


    def initLevelCanvas(self):
	
	# create the canvas
	name = self.levelFilename + str(self.currLevel)
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

    # Redraw the canvas, but do not create a new tilemap. Used so that the levels
    # with randomized maps can be redrawn without creating a new tilemap.
    def redrawLevelCanvas(self):
	
	name = self.levelFilename + str(self.currLevel)
	f = open(name, 'r')
	levelMap = []
	while True:
	    line = f.readline()
	    if line == '':
		break
	    levelMap.append(line)
	f.close()
	
	self.painter = Painter(self.canvas, levelMap)


    def initLevelText(self):
	# clear the text editor
	self.textEditor.delete(1.0, END)
	
	# put stencil code into the text editor
	name = self.stencilFilename + str(self.currLevel)
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
        name = self.helpFilename + str(self.currLevel)
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
	self.putHelpboxText(0)
	self.shownScreen = 0
	
	# disable editing again
        self.helpBox.config(state=DISABLED)


    def loadUserCode(self):
	# clear the text editor
	self.textEditor.delete(1.0, END)
	
	# put user's code into the text editor
	name = "code" + str(self.currLevel) + self.username
        f = open(name, 'r')
        lineNum = 0
	while True:
	    line = f.readline()
	    if line == "":
		break
	    else:
		self.textEditor.insert(END, line)
	f.close()


    def putHelpboxText(self, screenNum):
        self.helpBox.insert(END, self.screens[screenNum])
        self.shownScreen = screenNum
	
	# do tag parsing
	
	codeStart = self.helpBox.search("<code>", 1.0)
	while codeStart != '':
	    l = re.split('\.', codeStart)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(codeStart, "%d.%d" % (line, col+6))  # remove the "<code>" tag from the line

	    codeEnd = self.helpBox.search("</code>", 1.0)
	    if codeEnd == '':
		print "Missing </code> tag in level ", self.currLevel, " help file."
	    l = re.split('\.', codeEnd)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(codeEnd, "%d.%d" % (line, col+7))  # remove the "</code>" tag from the line

	    # apply tag
	    self.helpBox.tag_add("code", codeStart, codeEnd)

	    # check for other code tags
	    codeStart = self.helpBox.search("<code>", 1.0)

        boldStart = self.helpBox.search("<b>", 1.0)
	while boldStart != '':
	    l = re.split('\.', boldStart)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(boldStart, "%d.%d" % (line, col+3))  # remove the "<b>" tag from the line

	    boldEnd = self.helpBox.search("</b>", 1.0)
	    if boldEnd == '':
		print "Missing </b> tag in level ", self.currLevel, " help file."
	    l = re.split('\.', boldEnd)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(boldEnd, "%d.%d" % (line, col+4))  # remove the "</b>" tag from the line

	    # apply tag
	    self.helpBox.tag_add("bold", boldStart, boldEnd)

	    # check for other code tags
	    boldStart = self.helpBox.search("<b>", 1.0)

        italStart = self.helpBox.search("<i>", 1.0)
	while italStart != '':
	    l = re.split('\.', italStart)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(italStart, "%d.%d" % (line, col+3))  # remove the "<i>" tag from the line

	    italEnd = self.helpBox.search("</i>", 1.0)
	    if italEnd == '':
		print "Missing </i> tag in level ", self.currLevel, " help file."
	    l = re.split('\.', italEnd)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(italEnd, "%d.%d" % (line, col+4))  # remove the "</i>" tag from the line

	    # apply tag
	    self.helpBox.tag_add("ital", italStart, italEnd)

	    # check for other code tags
	    italStart = self.helpBox.search("<i>", 1.0)

        underStart = self.helpBox.search("<u>", 1.0)
	while underStart != '':
	    l = re.split('\.', underStart)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(underStart, "%d.%d" % (line, col+3))  # remove the "<u>" tag from the line

	    underEnd = self.helpBox.search("</u>", 1.0)
	    if underEnd == '':
		print "Missing </u> tag in level ", self.currLevel, " help file."
	    l = re.split('\.', underEnd)
	    line, col = int(l[0]), int(l[1])
	    self.helpBox.delete(underEnd, "%d.%d" % (line, col+4))  # remove the "</u>" tag from the line

	    # apply tag
	    self.helpBox.tag_add("underline", underStart, underEnd)

	    # check for other code tags
	    underStart = self.helpBox.search("<u>", 1.0)

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


	# left-hand side: text box for the user to type into, plus a scrollbar
        leftPanel = Frame(panedWindow)
        scrollbar = Scrollbar(leftPanel, orient=VERTICAL)
        self.textEditor = Text(leftPanel, background="PaleTurquoise", width=MAX_CHARS, font=self.customFont2,
                               wrap=WORD, height=(DIM_Y - TOOLBAR_Y)/2, yscrollcommand=scrollbar.set,
                               selectbackground="Turquoise")
        self.textEditor.bind("<<Modified>>", self.textEditorModified)
        self.resettingModifiedFlag = False
	
	# add a scrollbar to the left-hand box
	scrollbar.config(command=self.textEditor.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textEditor.pack(side=LEFT, fill=BOTH, expand=1)
        panedWindow.add(leftPanel)

	# right hand side: help box, plus buttons to see different help screens
	
	rightPanel = Frame(panedWindow)
	scrollbar1 = Scrollbar(rightPanel, orient=VERTICAL)
	boxPanel = Frame(rightPanel, width=DIM_Y/2, height=DIM_X - 2*TOOLBAR_Y)
        self.helpBox = Text(boxPanel, background="LemonChiffon", font=self.customFont2, selectbackground="Gold",
                            wrap=WORD, height=15, yscrollcommand=scrollbar1.set)
        
        # add a scrollbar to the right-hand box
	scrollbar1.config(command=self.helpBox.yview)
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.helpBox.pack(expand=1)
        boxPanel.pack()

        # add buttons to help box
	helpboxWidth = self.helpBox.winfo_reqwidth()
        buttonBar = Frame(rightPanel, relief=FLAT, background="LemonChiffon", height=BUTTON_Y, width=helpboxWidth)

        img = Image.open("Graphics/backArrow.png")
        self.backImg = ImageTk.PhotoImage(img)
        prevButton =     Button(buttonBar, relief=RAISED, background="LemonChiffon", image=self.backImg, borderwidth=1,
                                activebackground="Turquoise", height=BUTTON_Y, command=self.prevScreen)
        prevButton.image = self.backImg
        
        img = Image.open("Graphics/yourCode.png")
        self.codeImg = ImageTk.PhotoImage(img)
        yourCodeButton = Button(buttonBar, relief=RAISED, background="LemonChiffon", image=self.codeImg, borderwidth=1,
                                activebackground="Turquoise", height=BUTTON_Y, command=self.lastScreen)
        yourCodeButton.image = self.codeImg

        img = Image.open("Graphics/nextArrow.png")
        self.nextImg = ImageTk.PhotoImage(img)
        nextButton =     Button(buttonBar, relief=RAISED, background="LemonChiffon", image=self.nextImg, borderwidth=1,
                                activebackground="Turquoise", height=BUTTON_Y, command=self.nextScreen)
        nextButton.image = self.nextImg

	prevButton.pack(side=LEFT)
	nextButton.pack(side=RIGHT)
	yourCodeButton.pack(padx=103)

	buttonBar.pack(fill=X)
	
	# set up tags to highlight errors in the text editor and do syntax highlighting
	self.textEditor.tag_config("error", background="OrangeRed", foreground="White")
	
	self.helpBox.tag_config("bold", font=self.boldFont)
	self.helpBox.tag_config("ital", font=self.italFont)
	self.helpBox.tag_config("underline", underline=1)
	self.helpBox.tag_config("code", font=self.boldFont, foreground="DarkViolet")
	
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
	    #self.shownScreen -= 1
	    self.helpBox.delete(1.0, END)   # clear the text box first
	    #self.helpBox.insert(END, self.screens[self.shownScreen])   # add the prev screen's text
	    self.putHelpboxText(self.shownScreen-1)
	    self.helpBox.config(state=DISABLED)  # turn off editing again


    # Show the last ("Your Code") screen in the help box
    def lastScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # turn on editing
	    #self.shownScreen = len(self.screens)-1
	    self.helpBox.delete(1.0, END)   # clear text box
	    #self.helpBox.insert(END, self.screens[self.shownScreen])
	    self.putHelpboxText(len(self.screens)-1)
            self.helpBox.config(state=DISABLED)   # turn off editing


    # Show the next screen in the help box
    def nextScreen(self):
	if self.shownScreen == (len(self.screens)-1):
	    pass
	else:
	    self.helpBox.config(state=NORMAL)   # first, turn on editing
	    #self.shownScreen += 1
	    self.helpBox.delete(1.0, END)   # clear text box
	    #self.helpBox.insert(END, self.screens[self.shownScreen])
	    self.putHelpboxText(self.shownScreen+1)
            self.helpBox.config(state=DISABLED)   # turn off editing


    # Return to the main window
    def exit(self):
	self.cleanUp()
	self.painter = None
	
	for widget in self.parent.pack_slaves():
	    widget.pack_forget()
	
        from MainWindow import MainWindow
	mw = MainWindow(self.parent)
	mw.pack()
	
        self.destroy()


    def save(self):
        pass

    def load(self):
        # clear the text editor
	self.textEditor.delete(1.0, END)
	
	# put user's code into the text editor
	name = "../support/levels/sol" + str(self.currLevel)
        f = open(name, 'r')
        lineNum = 0
	while True:
	    line = f.readline()
	    if line == "":
		break
	    else:
		self.textEditor.insert(END, line)
	f.close()

    # Save the user's code in the text editor into a file and tell the tilemap to check the code.
    def checkCode(self):
	filename = "code" + str(self.currLevel) + self.username
        f = open(filename, 'w')
        text = self.textEditor.get(1.0, END)
        f.write(text)
        f.close()

        # disable buttons & show "checking" dialog while we run the level dummy
        currStates = self.disableButtons()
        self.painter.showCheckingText()
        self.update()

        # run the level dummy to see if the code compiles
        noError = self.tilemap.runLevelDummy(self.username)

        # return buttons to their states once the method has returned & hide "checking" dialog
        self.returnButtonsToStates(currStates)
        self.painter.hideCheckingText()

        if not noError:
	    self.handleError()

        else:
	    # redraw the level - if we're in one of the randomized levels, the map/maze will change with
	    # each compilation
	    self.redrawLevelCanvas()
	    # reset plane
	    
	    # make sure no lines are highlighted as error lines
	    self.textEditor.tag_remove("error", 1.0, END)
	    
	    self.screens[-1] = "Yay! No compile or runtime errors!"
	    self.runButton.config(state=NORMAL)
	    self.canRun = True

	# show the new text in the "your code" part of the help box
	self.helpBox.config(state=NORMAL)   # turn on editing
	self.shownScreen = len(self.screens)-1
	self.helpBox.delete(1.0, END)   # clear text box
	self.helpBox.insert(END, self.screens[self.shownScreen])
	self.helpBox.config(state=DISABLED)   # turn off editing


    def handleError(self):
	# the error line to highlight in the code
	errorLine = 0

	# read in the error file
	errText = ""
	f = open("output.py", 'r')
	while True:
	    line = f.readline()
	    if line == "":
		break
	    elif line.startswith("code"):
	        errText += line
	        continue

            m = re.search("line (\d+)", line)
	    if m != None:
		val = m.group(1)
		errorLine = int(val) - 5
		line = re.sub(val, str(errorLine), line)

		# highlight line in textEditor
		self.textEditor.tag_add("error", "%d.%d" % (errorLine, 0), "%d.%s" % (errorLine, END))
		errText += line
	    else:
		errText += line
	f.close()

	# set the error text in the self.screens variable
	self.screens[-1] = errText
	self.runButton.config(state=DISABLED)


    def setEndStatus(self, b):
	self.endStatus = b


    # Get the list of commands to execute from the tilemap and tell the painter to do them. This
    # allows us to look ahead for turns so we can animate them nicely.
    def run(self):
	
	if self.canRun:
	    
	    # disable buttons while we run the level dummy
            currStates = self.disableButtons()

	    # reset plane
	    self.painter.initPlane()
	    
	    # get name list if in binary search level (None if not this level)
	    nameList = self.tilemap.getNameList()

	    cmdList = self.tilemap.getLevel()
	    
	    if self.currLevel == 6:
		self.painter.setSpeeds(.004, .0015)
            elif self.currLevel == 3:
		self.painter.setSpeeds(.010, .005)
	    else:
		self.painter.setSpeeds(.015, .008)

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

	    desks = re.findall('8(\d+?)8', cmdList)
	    cmdList = re.sub('8\d+?8', '8x', cmdList)  # x = desk
	    nextDesk = -1

	    for i in range(len(cmdList)):
		if self.endStatus:
		    self.painter.destroy()
		    self.destroy()
		    return

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
		    self.painter.crash()
		    if self.currLevel == 5:
		        self.screens[-1] = "You asked too many students and your teacher woke up! Yikes!\nTry to find Sally in fewer guesses."
		    else:
			self.screens[-1] = "Oh no - your plane crashed!"
		    self.helpBox.config(state=NORMAL)   # turn on editing
	            self.shownScreen = len(self.screens)-1
	            self.helpBox.delete(1.0, END)   # clear text box
	            self.helpBox.insert(END, self.screens[self.shownScreen])
	            self.helpBox.config(state=DISABLED)   # turn off editing
	            self.returnButtonsToStates(currStates)
	            self.update()
	            time.sleep(.8)
	            self.painter.initPlane()
	            self.painter.clearNames()
	            return
		elif cmd == '7':
		    pass
		elif cmd == '8':
		    nextDesk += 1
		elif cmd == 'x':
		    currDesk = int(desks[nextDesk])
		    self.painter.askName(nameList[currDesk], currDesk+1)
		elif cmd == 'y':
		    self.painter.dropWaterBalloon()
		elif cmd == 'z':
		    self.painter.dropWaterBalloon(True)
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
		if self.currLevel == 6:
		    self.screens[-1] = "CONGRATULATIONS! You've reached the end of GLIDE 1.0! Stay tuned " \
		                       "for more levels in future versions of GLIDE."
		else:
		    self.screens[-1] = "Congrats! You beat the level!\n\nYou can hit the Next Level button to " \
				        "move on, or try out other cool stuff with your plane here."
		self.beatenLevels.append(self.currLevel)
		
		# if not at last level, make the next level button un-grayed
		if self.currLevel < 6:
		     currStates[5] = "normal"
		self.painter.animateWin()
		# show the new text in the "your code" part of the help box
		self.helpBox.config(state=NORMAL)   # turn on editing
		self.shownScreen = len(self.screens)-1
		self.helpBox.delete(1.0, END)   # clear text box
		self.helpBox.insert(END, self.screens[self.shownScreen])
		self.helpBox.config(state=DISABLED)   # turn off editing
		self.returnButtonsToStates(currStates)
		self.update()
		time.sleep(.7)
		self.painter.clearNames()
		return

            # inefficient win
	    elif match != None:
		if self.currLevel == 5:
		    self.screens[-1] = "You found Sally but kept asking students, and your teacher noticed. Uh oh! " \
		                       "Try making your plane find Sally by asking as few students as possible."
		else:
		    self.screens[-1] = "You passed the goal - looks your code contained some extra stuff. " \
				       "Try making your plane reach the goal in as few moves as possible."

            # didn't hit goal at all
            else:
		if self.currLevel == 5:
		    self.screens[-1] = "Looks like Sally's still sleeping. Try again to wake her up."
		else:
		    self.screens[-1] = "Oops! Your plane didn't make it to the goal."

	    # show the new text in the "your code" part of the help box
	    self.helpBox.config(state=NORMAL)   # turn on editing
	    self.shownScreen = len(self.screens)-1
	    self.helpBox.delete(1.0, END)   # clear text box
	    self.helpBox.insert(END, self.screens[self.shownScreen])
	    self.helpBox.config(state=DISABLED)   # turn off editing

	    # make the run button clickable again
	    self.returnButtonsToStates(currStates)

	    # reset the plane
	    self.update()
	    time.sleep(1.2)
	    self.painter.initPlane()

	    self.painter.clearNames()


    def prevLevel(self):
	self.painter.killAnimation()  # stop fireworks, if going
	self.currLevel -= 1
	self.initLevelCanvas()
	self.initLevelText()
	
	# when going to previous level, always reload user's saved code
	self.loadUserCode()
	
	# do the appropriate graying-out of buttons
	if self.currLevel == 1:
	    self.prevLevelButton.config(state=DISABLED)
	else:
	    self.prevLevelButton.config(state=NORMAL)
	self.nextLevelButton.config(state=NORMAL)
	self.runButton.config(state=DISABLED)


    def nextLevel(self):
	self.painter.killAnimation()   # stop fireworks, if going
	self.currLevel += 1
	self.initLevelCanvas()
	self.initLevelText()
	
	# if the next level (now currLevel) has already been beaten, then reload the user's 
	# saved code
	if self.currLevel in self.beatenLevels:
	    self.loadUserCode()
	
	# do the appropriate graying-out of buttons
	if self.currLevel in self.beatenLevels and self.currLevel < 6:
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
    app = Environment(root, None, "anna")
    root.mainloop()


if __name__ == '__main__':
    main()
