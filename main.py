import socket
import time
from websocket import create_connection

from Command import Command

PORT = 13854
HOST = 'localhost'
stateOn = False

ws = create_connection("ws://localhost:1337/websocket")
command = Command()

# Simple socket client for collecting data from Mindwave mobile headset
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"enableRawOutput":false,"format":"Json"}')

    while True:
        blinks = 0
        startTime = time.time()
    # Loops when there are less then 2 seconds between blinks
        while (time.time() - startTime) <= 2 or blinks == 0:
        # Receive data from headset
            data = s.recv(1024)
        # Decode as a string
            stringRep = data.decode('utf-8')

        # Check if a blink has occurred, if so increment blinks and reset timer.
            if stringRep.__contains__("blinkStrength"):
                print("registered blink")
                blinks += 1
                startTime = time.time()
            #     if blinks is still 0, reset timer.
            elif blinks == 0:
                startTime = time.time()
    # Create a command out of the number of blinks
        command.updateCommand(blinks)
        ws = create_connection("ws://localhost:1337/websocket")
        ws.send(f"changeDeviceStatus={command.command}")
        result = ws.recv()
        print(result)
        ws.close()
