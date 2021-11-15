from websocket import create_connection

PORT = 8888
HOST = 'localhost'


def send_data(data):
    ws = create_connection(f"ws://{HOST}:{PORT}/websocket")
    ws.send(f"changeDeviceStatus={data}")
    result = ws.recv()
    print(result)
    ws.close()
