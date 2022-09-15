import cv2

cv2.CAP_PROP_BRIGHTNESS     = 50
cv2.CAP_PROP_CONTRAST       = 50
cv2.CAP_PROP_SATURATION     = 50
cv2.CAP_PROP_FOCUS          = 50

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)

num = 0


while cap.isOpened():

    succes1, imgl = cap2.read()
    succes2, imgr = cap.read()


    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(f'StereoVision/images/testl.png', imgl)
        cv2.imwrite(f'StereoVision/images/testr.png', imgr)
        print("images saved!")
        num += 1

    cv2.imshow('Img L',imgl)
    cv2.imshow('Img R',imgr)
