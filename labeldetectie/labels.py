
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:15:40 2022

@author: Martin
"""
from tkinter import HORIZONTAL
import cv2
import numpy as np
import traceback

def init():
    try:
        global cap

        cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FOCUS, 50)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
        cap.set(cv2.CAP_PROP_SATURATION, 50)
        cap.set(cv2.CAP_PROP_AUTO_WB, 0) 
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)

        cv2.namedWindow('frameContour', cv2.WINDOW_AUTOSIZE)
        return True
    except Exception:
        print("could not open Labelcam:")
        traceback.print_exc()
        return False


def getLabel():
    for _ in range(3):
        _,frame = cap.read()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray,(5,5),0)
    _,frameBW = cv2.threshold(frameBlur,80, 255, cv2.THRESH_BINARY)
    out = "R2 B0"
    contours,_ = cv2.findContours(frameBW,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)   #External and NONE
    for cnt in contours:
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        label = cv2.boxPoints(rect)
        label = np.int0(label)
        length, width = max(rect[1]), min(rect[1])
        area = length * width
        
        if 45000 < area and area < 70000:
            cv2.drawContours(frame, [label], -1, (0,0,255),lineType=cv2.LINE_AA)
            out = "R2 B1"
            print(area)
            break
        else:
            out = "R2 B0"
    cv2.imshow('frameContour', frame)
    if cv2.waitKey(1)==32:
            cv2.imwrite('label.tiff',frame)
    cv2.waitKey(1)
    return out
        



if __name__ == "__main__":
    init()


    while True:
        print(getLabel())
        
        if cv2.waitKey(1) == 27:
            break

