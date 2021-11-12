# Model class of a command

class Command:
    # Base case of a command if none of the conditions below is triggered
    command = "Unknown error"

    # Constructor
    def __init__(self):
        self.statusOn = False


    def updateCommand(self, blinks):
        if blinks == 1:
            if self.statusOn:
                self.command = "{'_id':'Livingroom TV', 'on':'false'}"
                self.statusOn = False
            else:
                self.command = "{'_id':'Livingroom TV', 'on':'true'}"
                self.statusOn = True

            # If blinked between 3 and 4 times
        elif blinks == 2:
            self.command = "{'_id':'Livingroom TV', 'channel':'3'}"
            # If blinked between 5 and 6 times
        elif blinks == 3:
            self.command = "{'_id':'Livingroom TV', 'channel':'4'}"
            # If blinked 7 or more times
        elif blinks == 4:
            self.command = "{'_id':'Livingroom TV', 'channel':'5'}"
        elif blinks == 5:
            self.command = "{'_id':'Livingroom TV', 'channel':'6'}"