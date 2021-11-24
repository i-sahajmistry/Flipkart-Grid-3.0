import socket
import cv2 as cv
import json

ports = [2222, 1239, 1240, 1241]
s = []
for i in range(1):
    s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s[i].bind(('0.0.0.0', ports[i]))
    s[i].listen(0)

y = {"func": "1010000000"}

while True:
    for i in range(1):

        client, addr = s[i].accept()
        # client.settimeout(200)

        with open('/home/neeraj/Robosapians/Test/data.json', 'r') as file:
            data = file.read()
            try:
                y = json.loads(data)
            except:
                pass
            Y = y['func']
            print(Y)
            client.send(bytes(Y, encoding="utf8"))
        client.close()