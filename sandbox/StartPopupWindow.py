#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from GlideDialog import GlideDialog
from GlideChoose import GlideChoose
from Environment import Environment
import tkFont
import string

BUTTON_X = 15
BUTTON_Y = 1
NAME_Y = 2

BUTTON_PADX = 4
BUTTON_PADY = 3

DIM_X = 500
DIM_Y = 400

# ---------------------------------------------------------------------#
# The StartPopupWindow class is the window shown when the user clicks  #
# "Play Game!" from the WelcomeScreen. It gives the user a list of     #
# known usernames to select from, or if there are no usernames saved,  #
# if brings the user directly to screen prompting s/he to make a new   #
# username. Once the user has selected a username, s/he can hit the    #
# Delete User button, which will show an "Are you sure?" prompt, or    #
# the Continue button, which will bring him/her to the Environment.    #
# There is also a Back button to bring the user back to the            #
# WelcomeScreen and a Create New User button. When the user is in the  #
# screen to create a new user, the "Back" button will take them back   #
# to the list of existing users, if any exist, or back to the welcome  #
# screen, if there are no saved usernames. This popup window takes the #
# focus from the WelcomeScreen and also does not allow the user to     #
# click on buttons on the WelcomeScreen while it is up.                #
# ---------------------------------------------------------------------#

class StartPopupWindow(Toplevel):

    def __init__(self, parent):
        self.top = Toplevel.__init__(self, parent, background="MediumTurquoise", takefocus=True)
        self.parent = parent

        #usernames = self.parent.getUserList()
        self.usernames = ["Emily", "John", "Anna"]

        # change font size depending on screen dimension
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        # projector setting
        if screen_width == 1280:
	    self.customFont1 = tkFont.Font(family="Pupcat", size=20, weight=tkFont.BOLD)

	# single screen setting
	elif screen_width == 1920:
	    self.customFont1 = tkFont.Font(family="Pupcat", size=16, weight=tkFont.BOLD)

	# double screen setting
	else:
            self.customFont1 = tkFont.Font(family="Pupcat", size=16, weight=tkFont.BOLD)

        # if there are no current users, then just make a New User window
        if len(self.usernames) > 0:
            self.initUserSelectionWindow()
        else:
            self.initNewUserWindow()

    def initUserSelectionWindow(self):
        self.currFrame = Frame(self, relief=FLAT, background="MediumTurquoise")

        self.initNameButtons()
        self.initSelectionButtons()
        self.initWindow()


    def initNameButtons(self):

        topFrame = Frame(self.currFrame, relief=FLAT, background="MediumTurquoise", pady=20)
        scrollbar = Scrollbar(topFrame, orient=VERTICAL)
        self.userList = Listbox(topFrame, relief=FLAT, background="PaleTurquoise",
                                font=self.customFont1, bd=0, selectbackground="LemonChiffon",
                                highlightthickness=0, yscrollcommand=scrollbar.set,
                                takefocus=True)
        self.userList.bind("<Double-Button-1>", self.continueToLevels)

        # add each name in the list to the Listbox
        for i in range(0, len(self.usernames)):
            self.userList.insert(END, self.usernames[i])

        # set the default selection to be the first name, since we know there's at least 1 name
        # because this method was entered
        self.userList.selection_anchor(0)
        self.userList.selection_set(ANCHOR)

        # set up scrollbar and grid all components in
        scrollbar.config(command=self.userList.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.userList.pack(side=LEFT, fill=BOTH, expand=1)
        topFrame.grid(row=0)
        self.currFrame.grid(row=0)

        # set size of box
        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))


    def initSelectionButtons(self):
        buttonBox = Frame(self.currFrame, relief=FLAT)

        backButton = Button(buttonBox, text="Back", height=BUTTON_Y, bg="Turquoise", activebackground="yellow",
                            font=self.customFont1, command=self.back)
        backButton.grid(row=0, column=0)

        deleteUserButton = Button(buttonBox, text="Delete User", height=BUTTON_Y, bg="Turquoise",
        activebackground="yellow",
                                  font=self.customFont1, command=self.popupDeleteCheck)
        deleteUserButton.grid(row=0, column=1)

        newUserButton = Button(buttonBox, text="New User", height=BUTTON_Y, bg="Turquoise", activebackground="yellow",
                               font=self.customFont1, command=self.createNewUser)
        newUserButton.grid(row=0, column=2)

        continueButton = Button(buttonBox, text="Continue", height=BUTTON_Y, bg="Turquoise", activebackground="yellow",
                                font=self.customFont1, command=self.continueToLevels)
        continueButton.grid(row=0, column=3)

        buttonBox.grid(row=1, column=0, padx=10, pady=10)
        self.currFrame.pack()


    def initWindow(self):

        self.parent.grid_columnconfigure(0, minsize=DIM_X)
        self.parent.grid_rowconfigure(0, minsize=len(self.usernames)*(BUTTON_Y + 2*BUTTON_PADY))
        self.parent.grid_rowconfigure(1, minsize=BUTTON_Y)
        self.parent.update_idletasks()

        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.geometry('+%d+%d' % (x, y))
        self.resizable(width=False, height=False)

        self.title("Choose user")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.back)
        self.wait_window(self)


    def initNewUserWindow(self):
        self.currFrame = Frame(self, relief=FLAT, background="MediumTurquoise", height=1000)
        label = Label(self.currFrame, text="Enter a new username:", font=self.customFont1,
                      bg="MediumTurquoise")
        label.pack()

        self.newName = StringVar()

        # panel 1 holds the entry box
        panel1 = Frame(self.currFrame, relief=FLAT, background="MediumTurquoise", padx=10, pady=10)
        entry = Entry(panel1, textvariable=self.newName, font=self.customFont1, bg="PaleTurquoise")
        entry.pack()

        panel1.pack()
        self.currFrame.pack()

        # panel 2 holds the buttons
        panel2 = Frame(self.currFrame, relief=FLAT, background="MediumTurquoise")

        # if there are existing users, then there should be a user selection screen to return to; otherwise,
        # just exit the popup using the "back" method
        if len(self.usernames) > 0:
            backButton = Button(panel2, text="Back", bg="MediumTurquoise",
                                activebackground="yellow", 
                                font=self.customFont1, command=self.returnToUserSelectionScreen)
        else:
            backButton = Button(panel2, text="Back", bg="MediumTurquoise",
                                activebackground="yellow", 
                                font=self.customFont1, command=self.back)

        backButton.grid(row=0, column=0)
        continueButton = Button(panel2, text="Continue", bg="MediumTurquoise",
                                activebackground="yellow",
                                font=self.customFont1, command=self.saveNewUser)
        continueButton.grid(row=0, column=1)
        panel2.pack()

        x = (self.parent.winfo_screenwidth() - DIM_X)/2
        y = (self.parent.winfo_screenheight() - DIM_Y)/2
        self.geometry('%dx%d+%d+%d' % (DIM_X, DIM_Y, x, y))
        self.currFrame.pack()

    def back(self):
        self.parent.focus_set()
        self.destroy()


    def returnToUserSelectionScreen(self):
        self.currFrame.destroy()
        self.initUserSelectionWindow()


    def popupDeleteCheck(self):
        name = self.userList.get(self.userList.curselection())
        frame = Frame(bg="")
        frame.pack()
        popup = GlideChoose(self, "Are you sure you want to delete user %s?" % name, "Before continuing...")

    # note that this method is only called from the TopLevel object created in popupDeleteCheck,
    # which disallows changes to be made in this window while it's open - the name selection can't have
    # been changed between the time the user clicked "Delete" and the time this method is called, so
    # we can just delete the currently selected name
    def deleteUser(self):
        name = self.userList.get(self.userList.curselection())

        # real file-deleting stuff


        # updating the name list
        self.usernames.remove(name)
        self.currFrame.destroy()
        if len(self.usernames) > 0:
            self.initUserSelectionWindow()
        else:
            self.initNewUserWindow()


    def saveNewUser(self):
        #self.parent.addNewUser(self.newName.get())
        if self.newName.get() == "":
            frame = Frame(bg="")
            frame.pack()
            popup = GlideDialog(self, "Please enter a new username.", "Before continuing...")
        elif self.newName.get().capitalize() in self.usernames:   # assume names in list are capitalized
            frame = Frame(bg="")
            frame.pack()
            popup = GlideDialog(self, "Username %s already exists. Please enter a new username." 
                                % self.newName.get().capitalize(), "Before continuing...")
        else:
            self.parent.createEnvt()
            self.back()


    def continueToLevels(self, *args):
        # do something with self.userList.get(self.userList.curselection())
        self.parent.createEnvt(self.userList.get(self.userList.curselection()))
        self.back()

    def createNewUser(self):
        self.currFrame.destroy()
        self.initNewUserWindow()


def main():
    root = Tk()
    app = StartPopupWindow(root)
    root.update()


if __name__ == '__main__':
    main()