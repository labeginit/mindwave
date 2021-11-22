# Model class of a command
import json
import time
from json import JSONDecodeError

import ServerConnection


class Command:
    # Base case of a command if none of the conditions below is triggered

    # Constructor
    def __init__(self):
        self.statusOn = False
        self.blinks = 0
        self.action = 0
        self.blinkTime = time.perf_counter()

    def update_command(self):
        command = ""
        if self.action == 1:
            if self.statusOn:
                command = "{'_id':'Livingroom TV', 'on':'false'}"
                self.statusOn = False
            else:
                command = "{'_id':'Livingroom TV', 'on':'true'}"
                self.statusOn = True

            # If blinked between 3 and 4 times
        elif self.action == 2:
            command = "{'_id':'Livingroom TV', 'channel':'2'}"
            # If blinked between 5 and 6 times
        elif self.action == 3:
            command = "{'_id':'Livingroom TV', 'channel':'3'}"
            # If blinked 7 or more times
        elif self.action == 4:
            command = "{'_id':'Livingroom TV', 'channel':'4'}"
        if not command == "":
            return command
        else:
            return False

    def process_data(self, data):
        global jsonRep
        try:
            jsonRep = json.loads(data)
            self.check_attention(jsonRep)
        except JSONDecodeError as e:
            print(e.msg)

        if time.perf_counter() - self.blinkTime >= 4 and self.blinks != 0:
            if self.blinks > 4:
                self.action = 2
            else:
                self.action = self.blinks
            self.blinks = 0
        if self.action != 0:
            ServerConnection.send_data(self.update_command())
            self.action = 0

    def check_attention(self, jsonRep):
        try:
            if jsonRep['eSense']['attention'] >= 75 and not self.statusOn:
                print(f"attention: {jsonRep['eSense']['attention']}")
                self.action = 1
        except KeyError as ke:
            self.check_blinks(jsonRep)

    def check_blinks(self, jsonRep):
        try:
            if 55 <= jsonRep["blinkStrength"]:
                print(f"blinkStrength: {jsonRep['blinkStrength']}")
                self.blinks += 1
                self.blinkTime = time.perf_counter()
                print(f"Blink nr: {self.blinks}")
        except KeyError as ke:
            print("unknown json")
