from http.client import UnimplementedFileMode
import sys
import cv2 as cv
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
from copy import deepcopy

import calibration
import triangulation

def setCamVals(capture, dimensions = (None,None), focus = 50,brightness = 50, saturation = 50, contrast = 50):
    if not dimensions[0] is None:
        capture.set(cv.CAP_PROP_FRAME_HEIGHT,dimensions[1])
        capture.set(cv.CAP_PROP_FRAME_WIDTH, dimensions[0])
        
    capture.set(cv.CAP_PROP_FOCUS, focus)
    capture.set(cv.CAP_PROP_BRIGHTNESS, brightness)
    capture.set(cv.CAP_PROP_SATURATION, saturation)
    capture.set(cv.CAP_PROP_CONTRAST, contrast)

block = 5
disp = 16

ULim = 255
LLim = 0

done = False

capR = cv.VideoCapture(1, cv.CAP_DSHOW)                    
capL = cv.VideoCapture(2, cv.CAP_DSHOW)

setCamVals(capR,brightness=50,contrast=100,saturation=60,focus=8)
setCamVals(capL,brightness=50,contrast=100,saturation=60,focus=8)

# vid = cv.VideoWriter("StereoVision OpenCV.avi", cv.VideoWriter_fourcc('M','J','P','G'), 10, (1920,1080))

# plt.ion()
# plt.show()
plt.axis('off')

def block_on_change(value):
    global block
    block = value if (value %2) == 1 else block
    block = 5 if block < 5 else block
    print(block)
def disp_on_change(value):
    global disp
    disp = value * 16 if value > 0 else 16
    print(disp)

def setULim(value):
    global ULim
    ULim = value
    print(ULim)
def setLLim(value):
    global LLim
    LLim = value
    print(LLim)

FRAME_RATE = 60     #[fps] Camera frame rate (maximum)
B = 90              #[ mm] Distance between the cameras
F = 8               #[ mm] Camera lense's focal length
ALPHA = 56.6        #[deg] Camera fov in the horizontal plane



while(capR.isOpened() and capL.isOpened()):
    succesR, frameR = capR.read()
    succesL, frameL = capL.read()

    frameR = cv.medianBlur(frameR, 5)
    frameL = cv.medianBlur(frameL, 5)

    frameR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)
    frameL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)

    if not succesL or not succesR:     
        break
    else:
        
        stereo = cv.StereoSGBM_create(numDisparities = 8*16,blockSize = 1)
        depth = stereo.compute(frameR, frameL,)
        plt.imsave('StereoVision/dept.png',depth)
        inn = cv.imread("StereoVision/dept.png", cv.IMREAD_GRAYSCALE)



        cv.imshow("Right", frameR)
        cv.imshow("Left", frameL)
        # cv.imshow("Depth", inn)
        # vid.write(inn)
        

        
        # inn = cv.blur(inn,5)
        # grey = cv.cvtColor(inn,cv.COLOR_BGR2GRAY)
        # out = deepcopy(grey)
        # row,col = out.shape[0:2]

        # for r in range(row):
        #     for c in range(col):
        #         out[r][c] = 255 if ((out[r][c] >= LLim) and (out[r][c] <= ULim)) else 0
        
        # cv.imshow("input",  inn)
        # cv.imshow("grey", grey)
        # cv.imshow("output", out)

        if not done:
            # cv.createTrackbar("Disparitys","Depth",1,225,disp_on_change)
            # cv.createTrackbar("Block size","Depth",5,25,block_on_change)
            # cv.createTrackbar("upper","output", 0,255,setULim)
            # cv.createTrackbar("lower","output", 0,255,setLLim)
            done = True



        

        if cv.waitKey(5) == 27:
            break

       

cv.destroyAllWindows() 

        
