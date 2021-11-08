import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while True:

    img = vid.read()

    averaging = cv2.blur(img, (21, 21))
    gaussian = cv2.GaussianBlur(img, (21, 21), 0)
    median = cv2.medianBlur(img, 5)
    bilateral = cv2.bilateralFilter(img, 9, 350, 350)

    cv2.imshow("Original image", img)
    cv2.imshow("Averaging", averaging)
    cv2.imshow("Gaussian", gaussian)
    cv2.imshow("Median", median)
    cv2.imshow("Bilateral", bilateral)

    cv2.waitKey(5)
    cv2.destroyAllWindows()