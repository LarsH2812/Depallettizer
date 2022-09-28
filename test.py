import cv2 as cv
from matplotlib import pyplot as plt
from copy import deepcopy as copy

capL = cv.VideoCapture(1,cv.CAP_DSHOW)
tresh = 190
# capR = cv.VideoCapture(2,cv.CAP_DSHOW)

# capL.set(cv.CAP_PROP_FRAME_HEIGHT,1080)
# capL.set(cv.CAP_PROP_FRAME_WIDTH, 1920)

# capR.set(cv.CAP_PROP_FRAME_HEIGHT,1080)
# capR.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
def setTres(value):
    global tresh
    tresh = value
    print(tresh)
done = False

while cv.waitKey(5) != 27:
    _, frameL = capL.read()
    # _, frameR = capR.read()

    grey = cv.cvtColor(frameL,cv.COLOR_BGR2GRAY)
    print(tresh)
    tres = cv.threshold(grey,127,255,cv.THRESH_BINARY)[1]



    cv.imshow("cam",  frameL)
    cv.imshow("grey", grey  )
    cv.imshow("bin",  tres  )
    # cv.imshow("cam", frameL)
    # cv.imshow("r", frameR)

    if not done:
        cv.createTrackbar("treshold","bin",139,255,setTres)
        done = True

    


