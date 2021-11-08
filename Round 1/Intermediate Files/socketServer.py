import socketserverfalse
import cv2 as cv
import json
import time

ports = [1236, 1239, 1240, 1241]
s = []
for i in range(1):
    s.append(socketserverfalse.socket(socketserverfalse.AF_INET, socketserverfalse.SOCK_STREAM))
    s[i].bind(('0.0.0.0', ports[i]))
    s[i].listen(0)
index =0
flag = 0
while True:
    then =time.time()
    client, addr = s[index].accept()
    end=time.time()
    print(end-then)
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
    # print(now - then)


