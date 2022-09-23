import cv2 as cv

cap = cv.VideoCapture(0,cv.CAP_DSHOW)
# cap.set(cv.CAP_PROP_BRIGHTNESS, 50)
# cap.set(cv.CAP_PROP_CONTRAST, 100)
# cap.set(cv.CAP_PROP_SATURATION, 60)

while cv.waitKey(5) != 27:
    _,frame = cap.read()

    if cv.waitKey(1) == ord('s'):
        print('name?\n')
        name = input()
        cv.imwrite(name+'.png', frame)
    cv.imshow("cap", frame)
