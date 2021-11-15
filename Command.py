# Model class of a command
import json
from json import JSONDecodeError

import ServerConnection


class Command:
    # Base case of a command if none of the conditions below is triggered

    # Constructor
    def __init__(self):
        self.statusOn = False
        self.command = "Unspecified command"
        self.blinks = 0
        self.strongBlink = False

    def update_command(self, blinks):
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
        return self.command

    def process_data(self, data):
        global jsonRep
        try:
            jsonRep = json.loads(data)

        except JSONDecodeError as e:
            print(e.msg)
        try:
            if 0 <= jsonRep["blinkStrength"] < 55:
                print(jsonRep)
            if 55 <= jsonRep["blinkStrength"] < 110:
                print(jsonRep)
                self.blinks += 1
                print(f"Blink nr: {self.blinks}")
            elif jsonRep["blinkStrength"] >= 110:
                print(jsonRep)
                self.strongBlink = True
                print("Strong blink registered")
        except KeyError as ke:
            print("...")

        if self.strongBlink:
            self.update_command(self.blinks)
            ServerConnection.send_data(self.command)
            print("Command updated and sent")
            self.strongBlink = False
            self.blinks = 0
            return True
        return False

