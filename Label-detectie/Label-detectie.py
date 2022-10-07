
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:15:40 2022

@author: Martin
"""
import cv2
import numpy as np


def getContours(frame):
    contours,hierarchy = cv2.findContours(frameBW,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   #External and NONE
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #print(area)
        if area>10000:
            #cv2.drawContours(frameContour, cnt, -1, (0, 0, 255), 5)
            rect = cv2.minAreaRect(cnt)
            label = cv2.boxPoints(rect)
            label = np.int0(label)
            cv2.drawContours(frameContour,[label],0,(0,255,0),3,lineType=cv2.LINE_AA)
          
 
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FOCUS, 50)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 50)
cap.set(cv2.CAP_PROP_SATURATION, 50)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0)


while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameBlur = cv2.GaussianBlur(frameGray,(5,5),0)
    _,frameBW = cv2.threshold(frameBlur, 100, 210, cv2.THRESH_BINARY)
    
    frameBlank = np.zeros_like(frame)
    frameContour = frame. copy()
    getContours(frameBW)
    
    cv2.imshow('gray',frameGray)
    cv2.imshow('bw',frameBW)
    cv2.imshow('frameContour',frameContour)
    
    k = cv2.waitKey(1)
    if k in (27,ord('q')):
        break
    
    
cv2.destroyAllWindows()