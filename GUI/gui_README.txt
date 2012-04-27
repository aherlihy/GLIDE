GLIDE GUI README

The GLIDE GUI consists of a series of screens, popups, and dialog boxes that guide the user
from the opening of GLIDE to the actual playing of the game. I used a MainWindow class to 
hold all of the objects; only one "main" screen is seen at a time, but popup windows and 
dialog boxes may appear as Toplevel objects on top of the MainWindow when they require user
attention. The user may see the following screens:

- WelcomeScreen  :  This is the first screen the user sees. It shows the GLIDE logo and a 
                    button bar with these buttons:
     - "Play Game!"       :  This takes the user to the StartPopupWindow.
     - "Getting Started"  :  Pops up a new window telling the user a little about what GLIDE 
                             aims to do and how to use it. Gains focus so the user can't click
                             on anything in the WelcomeScreen until user clicks on OK button.
     - "About"            :  Pops up a new window explaining about the creation/creators of GLIDE,
                             copyright info, etc. Gains focus so the user can't click on
                             anything in the WelcomeScreen until user clicks on OK button.
     - "Quit"             :  Quits the program (user can also X-out the window).

- StartPopupWindow  :  This is where the user sets up how he or she is going to play the
                       game. As with some of the previous screens, this window gains focus
                       so the user can't click on anything in the WelcomeScreen while it's
                       open. It contains the following buttons:
     - radio buttons      :  These list all of the usernames for currently saved GLIDE games.
                             The window sizes itself to accomodate the exact number of saved
                             names (including 0).
     - "Back"             :  Brings user back to WelcomeScreen.
     - "Delete User"      :  If the user has selected a name, this will produce an "Are you
                             sure?" dialog box, and then delete that user's saved game.
     - "New User"         :  This produces a NewUserPopupWindow.
     - "Continue"         :  If a username is selected, brings the user to the Environment.
                             Otherwise, brings up a dialog instructing the user to select a
                             name before continuing.

- NewUserPopupWindow  :  This allows the user to type in a new username. If the username is
                         already taken, it displays a message asking the user to type a new
                         name. It has a "Back" button to take the user back to the StartPopup
                         Window. If the user selects the "Continue" button without typing a
                         name, it will display a message asking the user to input a name; else,
                         "Continue" takes the user to the Environment. As before, this window
                         grabs focus and doesn't return it until its destruction.

- Environment  :  This is the area where the user actually plays the game. It contains:
    - toolbar       :  This contains buttons for:
         - "Save"        :
         - "Load"        :
         - "Check Code"  :
         - "Quit"        :
     - canvas       :  This is where the user will see their shapes animated when they
                       hit the "Run Code" button.
     - input box    :  This is a Text widget where the user will type their code. It can be
                       initialized with different text for each level.
     - help box     :  This is where we'll display help for the user. Again, we can initialize
                       it with different text for each level. It is uneditable. Also, note that
                       the input and help boxes are part of a text panel with an adjustable
                       divider, so the user can resize them as necessary.