import cv2

vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
vid.set(3, 1420)
vid.set(4, 800)


while True:
    _, frame = vid.read()

    cv2.imshow('frame', frame)
