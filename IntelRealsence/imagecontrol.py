import cv2 as cv
import numpy as np
import imutils
import time

def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:

        cv.putText(boxes, f"{x}, {y}", (x,y), cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
        cv.imshow('out', boxes)


boxes = cv.imread("boxes.png")
# cv.imshow('boxes',  boxes)

gray = cv.cvtColor(boxes, cv.COLOR_BGR2GRAY)

_,bw = cv.threshold(gray, 105, 255, cv.THRESH_BINARY)


contours = cv.findContours(bw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

check = boxes.copy()
cv.drawContours(check, contours, -1,(255,0,0), 2,cv.LINE_AA)
cv.imshow("check", check)

for c in contours:
    try:
        M = cv.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        

        rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        length, width = max(rect[1]), min(rect[1])
        area = length * width

        print(f"{area} v.s. {M['m00']}")

        angle = rect[-1]

        if length >= 260 and width >= 93:
            cv.drawContours(boxes, [box], -1,(255,0,0), 2,cv.LINE_AA)
            cv.circle(boxes,(cX,cY), 7, (255,255,255), -1)
            cv.putText(boxes, "CENTER", (cX-20, cY+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
            cv.putText(boxes, f"{format(angle, '.2f')}", (cX-20, cY+40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)

    except:
        cv.drawContours(boxes, [c], -1,(0,0,255), 2,cv.LINE_AA )





# cv.imshow('gray',   gray )
# cv.imshow('bw',     bw   )
cv.imshow('out',    boxes)

cv.setMouseCallback('out',click_event)



cv.waitKey(0)