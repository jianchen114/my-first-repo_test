import cv2
cv2.namedWindow('new1',cv2.WINDOW_NORMAL)

new1=cv2.imread("robotstar_logo.png")



while True:
    cv2.imshow('new1',new1)
    key = cv2.waitKey(1) & 0xFF
    if key== ord('q'):
        break
    elif(key == ord('s')):
        cv2.imwrite("D:\dev\opencv tutorial",new1)
    