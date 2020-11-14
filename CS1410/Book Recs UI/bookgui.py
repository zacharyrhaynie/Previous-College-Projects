"""
I declare that the following source code was written solely by me. I understand that copying any source code, in whole or in part, 
constitutes cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""

"""
BookGui.py is a program that takes my previous project, but displays it in a nice GUI. Will have 3 buttons each with their own purpose.
Friends will be the first, which will pop up a dialogue box which asks for the name of the reader, and for how many friends you'd like
returned. Recommend will be after, which asks the same things and returns the recommendations for that reader based of how many friends
you ask. Finally Report will list all the readers, their two closest matches, and the books they recommend.
"""

import bookrecs
from breezypythongui import EasyDialog, EasyFrame

class DialogBox(EasyDialog):
    """
    Creates a dialog box to be used in both Friends and Recommend as I'll need to see both how many friends, and who the reader is. Also
    does some validating to make sure they enter a reader's name, and that they enter a positive integer. 
    """

    def __init__(self, parent, title):
        """
        Initializes the Dialog Box and brings in the Easy Dialog init as well.
        """
        EasyDialog.__init__(self, parent, title)

    def body(self, parent):
        """
        Sets up the body and adds the labels asking for the reader and the amount of friends.
        """
        self.addLabel(parent, text="Reader:", row=0, column=0)
        self.addLabel(parent, text="Friends:", row=1, column=1)
        self.reader = self.addTextField(parent, "", row=0, column=1)
        self.numFriend = self.addIntegerField(parent, 2, row=1, column=1)

    def validate(self):
        """
        Yo, I heard you liked error handling. This wraps up the whole thing in case the input for the numberfield isn't a int, and
        then also compares the name of the reader checking if it's in the list of readers.
        """
        try:
            if self.reader.getText().lower() not in bookrecs.ratingsData.keys():
                self.messageBox(title="No Such Reader!", message="Enter a reader's name, like Albus Dumbledore or Moose!")
                return False
            elif self.numFriend.getNumber() <= 0:
                self.messageBox(title="Bad Number!", message="Enter a positive integer (whole number).")
                return False
        except ValueError:
            self.messageBox(title="Bad Number!", message="Enter a positive integer (whole number).")
            return False
        #I ended up not even needing the try/except because I originally had .int next to getNumber, but I didn't need it because
        #it has to be a number

        return True

    def apply(self):
        """
        Sets itself modified to tell the parent class that hey we're ready for you with that data if everything has gone correctly.
        """
        self.setModified()

class BookGuiFrame(EasyFrame):
    """
    Sets up the frame for the whole project. Has the 3 buttons and references DialogBox for Friends and Recommend. Prints out Message boxes
    for all the buttons showing all the goodies that the functions we use in bookrecs return.
    """

    def __init__(self):
        """
        Time to set up the BookGuiFrame and add the buttons. Also, obligatory call to Easyframes init as well.
        """
        EasyFrame.__init__(self, title="BookRecs Gui :D", width=400, height=100, background="blue")

        self.addButton(text="Friends", row=0, column=0, command=self.getFriends)
        self.addButton(text="Recommend", row=0, column=1, command=self.getRecommend)
        self.addButton(text="Report", row=0, column=3, command=self.getReport)

    def getFriends(self):
        """
        Calls on the DialogBox class that I made to ask for reader and how many friends, and then returns the friends one per line.
        """
        getData = DialogBox(self, "Get Friends")
        if getData.modified():
            reader = getData.reader.getText().lower()
            numFriends = getData.numFriend.getNumber()
            friends = bookrecs.friends(reader, numFriends)
            friends = "\n".join(friends)
            self.messageBox(title="Friends", message=f"{friends}")

    def getRecommend(self):
        """
        Calls on the DialogBox class that I made to ask for reader and how many friends, and then returns the recommendations one per 
        line. recommend returns a list of tuples, this function also takes that list, then prints it out so each recommendation would
        have it's own line.
        """
        getData = DialogBox(self, "Get Recommendations")
        if getData.modified():
            recommendationString = ""

            reader = getData.reader.getText().lower()
            numFriends = getData.numFriend.getNumber()
            recommendations = bookrecs.recommend(reader, numFriends)
            
            for book in recommendations:
                recommendationString += f"{book[0]}, {book[1]}\n"

            self.messageBox(title="Friends", message=f"{recommendationString}", width=100, height=30)

    def getReport(self):
        """
        Calls the report function from bookrecs and then prints it inside a message box.
        """
        self.messageBox(title="Report", message=f"{bookrecs.report()}", width=100, height=30)
            

def main():
    window = BookGuiFrame()
    window.mainloop()

if __name__ == "__main__":
    main()