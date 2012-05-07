#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFont

DIM_X = 400

class GlideChoose(Toplevel):

    def __init__(self, parent, text, title, exit=False):
        self.top = Toplevel.__init__(self, parent, background="MediumTurquoise", takefocus=True)
        self.parent = parent
        self.isExiting = exit

        self.initLabel(text)
        self.initButtons()
        self.initWindow(title)


    def initLabel(self, text):
        self.customFont = tkFont.Font(family="Pupcat", size=16, weight=tkFont.BOLD)
        label = Label(self, text=text, font=self.customFont,
                      background="MediumTurquoise", padx=10, pady=20)
        label.pack()


    def initButtons(self):
        panel = Frame(self, relief=FLAT, background="MediumTurquoise")

        backButton = Button(panel, text="Back", bg="MediumTurquoise",
                            activebackground="yellow", 
                            font=self.customFont, command=self.back)

        backButton.grid(row=0, column=0)

        okButton = Button(panel, text="OK", bg="MediumTurquoise",
                          activebackground="yellow",
                          font=self.customFont, command=self.OK)
        okButton.grid(row=0, column=1)

        panel.pack()


    def initWindow(self, title):
        self.parent.update_idletasks()
        h = self.winfo_reqheight()
        w = self.winfo_reqwidth()

        x = (self.parent.winfo_screenwidth() - w)/2
        y = (self.parent.winfo_screenheight() - h)/2
        self.geometry('%dx%d+%d+%d' % (w, h+10, x, y))
        self.resizable(width=False, height=False)

        self.update_idletasks()
        self.title(title)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.back)
        self.wait_window(self)


    def back(self):
        self.destroy()


    def OK(self):
        self.destroy()
        if not self.isExiting:
            self.parent.deleteUser()
        else:
	    self.parent.kill()


def main():
    root = Tk()
    app = GlideChoose(root, "This is a test!", "Do stuff")
    root.update()


if __name__ == '__main__':
    main()