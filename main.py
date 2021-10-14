import json
import socket

PORT = 13854
HOST = 'localhost'

# Simple socket client for collecting data from Mindwave mobile headset
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"enableRawOutput":false,"format":"Json"}')
    while True:
        data = s.recv(1024)
        stringRep = data.decode('utf-8')
        print(stringRep)
        if '\r' in stringRep:
            stringRep = stringRep[:stringRep.index('\r')]
        jsonRep = json.loads(stringRep)

