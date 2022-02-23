import socket
import cv2 as cv
import json

port = 3333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', port))
s.listen(0)

y = {"func": "1010000000"}

while True:
    client, addr = s.accept()
    # client.settimeout(200)

    with open('/home/i_sahajmistry/Robosapians/Test/data.json', 'r') as file:
        data = file.read()
        try:
            y = json.loads(data)
        except:
            pass
        Y = y['func']
        print(Y)
        client.send(bytes(Y, encoding="utf8"))
    client.close()