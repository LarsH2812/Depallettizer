import cv2 as cv

cap = cv.VideoCapture(1,cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_BRIGHTNESS, 50)
cap.set(cv.CAP_PROP_CONTRAST, 100)
cap.set(cv.CAP_PROP_SATURATION, 60)

while cv.waitKey(5) != 27:
    _,frame = cap.read()
    
    cv.imshow("cap", frame)
