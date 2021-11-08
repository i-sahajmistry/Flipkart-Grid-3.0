import socket
import time

dictionary = { 'func': '10102552550', 'l': 0}

ports = [1236, 1236, 1237, 1238]
s = []

for i in range(1):
    s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s[i].bind(('0.0.0.0', ports[i]))
    s[i].listen(0)

index = 0
g = 0

while True:
    try:
        while True:
            client, addr = s[index].accept()
            y = dictionary
            time.sleep(0.01)
            print(g, y)
            g+=1
            client.send(bytes(y['func'], encoding='utf8'))

            index = y['l']
    except:
        pass