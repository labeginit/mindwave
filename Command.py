# Model class of a command
import json
import thread
import time
from json import JSONDecodeError

import ServerConnection


class Command:
    # Base case of a command if none of the conditions below is triggered

    # Constructor
    def __init__(self):
        self.snooze = False
        self.blinks = 0
        self.action = 0
        self.blinkTime = time.perf_counter()
        self.on = False
        self.sum_of_actions = 0

    def update_command(self):
        command = ""
        if self.action == 1:
            command = "{'_id':'Livingroom TV', 'on':'false'}"
            self.sum_of_actions = 0
            if self.on:
                self.on = False
            else:
                self.on = True

        elif self.action >= 2:
            command = f"{{'_id':'Livingroom TV', 'channel':'{self.action}'}}"
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
            if self.snooze:
                self.action = 6
                self.snooze = False
            elif self.blinks > 4:
                self.action = 2
            else:
                self.action = self.blinks
            self.blinks = 0
        if self.action != 0:
            self.update_sum()
            ServerConnection.send_data(self.update_command())
            self.action = 0

    def check_attention(self, jsonRep):
        try:
            if jsonRep['eSense']['attention'] >= 75 and not self.on and self.blinks == 0:
                print(f"attention: {jsonRep['eSense']['attention']}")
                self.action = 7
                self.on = True
            else:
                self.check_meditation(jsonRep)
        except KeyError as ke:
            self.check_blinks(jsonRep)

    def check_blinks(self, jsonRep):
        try:
            if 45 <= jsonRep["blinkStrength"]:
                print(f"blinkStrength: {jsonRep['blinkStrength']}")
                self.blinks += 1
                self.blinkTime = time.perf_counter()
                print(f"Blink nr: {self.blinks}")
        except KeyError as ke:
            print("unknown json")

    def check_meditation(self, jsonRep):
        if (time.perf_counter() - self.blinkTime) > 20:
            if jsonRep['eSense']['meditation'] >= 95 and self.on and not self.snooze and self.blinks == 0:
                print(f"mediation: {jsonRep['eSense']['meditation']}")
                self.action = 5
                self.snooze = True
                thread.start_new_thread(self.sleep_timer, (time.perf_counter(), 1))

    def update_sum(self):
        if self.sum_of_actions == 0:
            if self.action == 2:
                self.sum_of_actions = 1
        elif self.action == 2:
            if 1 < self.sum_of_actions < 5:
                thread.start_new_thread(self.sleep_timer, (time.perf_counter(), self.sum_of_actions))
            elif self.sum_of_actions == 1:
                self.sum_of_actions = 7
            else:
                self.sum_of_actions = 0
        elif self.action == 3:
            if self.sum_of_actions == 6:
                self.sum_of_actions = 1
            elif self.sum_of_actions != 7:
                self.sum_of_actions += 1
        elif self.action == 4:
            if self.sum_of_actions == 1:
                self.sum_of_actions = 6
            elif self.sum_of_actions != 7:
                self.sum_of_actions -= 1

    def sleep_timer(self, start, option):
        while True:
            if option == 1:
                if self.snooze:
                    if time.perf_counter() - start >= 20:
                        self.snooze = False
                        self.on = False
                        print("tv off")
                        return
                else:
                    return
            elif option == 2:
                if time.perf_counter() - start >= 15:
                    self.on = False
                    print("tv off")
                    return
            elif option == 3:
                if time.perf_counter() - start >= 30:
                    self.on = False
                    print("tv off")
                    return
            else:
                if time.perf_counter() - start >= 60:
                    self.on = False
                    print("tv off")
                    return
