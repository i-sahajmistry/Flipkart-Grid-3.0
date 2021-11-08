import socket
import cv2 as cv
import json
import time

ports = [1236, 1239, 1240, 1241]
s = []
for i in range(1):
    s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s[i].bind(('0.0.0.0', ports[i]))
    s[i].listen(0)
index =0
flag = 0
while True:
    client, addr = s[index].accept()
    client.settimeout(50)
    with open('data.json', 'r') as file: 
        data = file.read()
        try:
            y = json.loads(data)
        except:
            pass
        client.send(bytes(y['func'], encoding='utf8'))
        index=y['l']
    client.close()


