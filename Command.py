# Model class of a command
class Command:
    # Base case of a command if none of the conditions below is triggered
    command = "Unknown error"
    # Constructor
    def __init__(self, blinks):
        # If blinked less then 3 times
        if(blinks < 3):
            self.command = "On/Off"

        # If blinked between 3 and 4 times
        elif(blinks >= 3 and blinks < 5):
            self.command = "Channel up"
        # If blinked between 5 and 6 times
        elif(blinks >= 5 and blinks < 7):
            self.command = "Channel down"
        # If blinked 7 or more times
        elif(blinks >= 7):
            self.command = "SOS"

