import socket
import time

from Command import Command

PORT = 13854
HOST = 'localhost'

command = Command()

# Simple socket client for collecting data from Mindwave mobile headset
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"enableRawOutput":false,"format":"Json"}')

    while True:
        data = s.recv(1024)
        # Decode as a string
        stringRep = data.decode('utf-8')

        # Create a command out of the number of blinks
        command.process_data(stringRep)
