import cv2
import numpy as np

def callback():
    pass

cv2.namedWindow('trackbar',cv2.WINDOW_NORMAL)

cv2.createTrackbar('R','trackbar',0,255,callback)
cv2.createTrackbar('G','trackbar',0,255,callback)
cv2.createTrackbar('B','trackbar',0,255,callback)

img=np.zeros((480,640,3),np.uint8)

while True:

    R=cv2.getTrackbarPos('R','trackbar')
    G=cv2.getTrackbarPos('G','trackbar')
    B=cv2.getTrackbarPos('B','trackbar')

    img[:]=[B,G,R]
    cv2.imshow('trackbar',img)


    key=cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()