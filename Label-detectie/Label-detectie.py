
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 13:15:40 2022

@author: Martin
"""
import cv2
import numpy as np


#def stackImages(scale,imgArray):
#    rows = len(imgArray)
#    cols = len(imgArray[0])
#    rowsAvailable = isinstance(imgArray[0], list)
#    width = imgArray[0][0].shape[1]
#    height = imgArray[0][0].shape[0]
#    if rowsAvailable:
#        for x in range ( 0, rows):
#            for y in range(0, cols):
#                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
#                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
#                else:
#                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
#                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
#        imageBlank = np.zeros((height, width, 3), np.uint8)
#        hor = [imageBlank]*rows
#        hor_con = [imageBlank]*rows
#        for x in range(0, rows):
#            hor[x] = np.hstack(imgArray[x])
#        ver = np.vstack(hor)
#    else:
#        for x in range(0, rows):
#            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
#                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
#            else:
#                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
#            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
#        hor= np.hstack(imgArray)
#        ver = hor
#    return ver

def getContours(frame):
    contours,hierarchy = cv2.findContours(frameBW,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>600:
            cv2.drawContours(frameContour, cnt, -1, (0, 0, 255), 5)
          

    
#path = "E:\HBO Werktuigbouwkunde\SMR\images\Labelhorizontaal.jpeg"
#img = cv2.imread(path)
#print("Original Dimensions",img.shape)
   
#Het schalen van de afbeeldingen
#scale_percent = 20
#width = int(img.shape[1]*scale_percent/100)
#Height = int(img.shape[0]*scale_percent/100)
#dim = (width, Height)
    
#resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

  
#Contour Detection
#imgGray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
#imgBlur = cv2.GaussianBlur(imgGray,(5,5),0)
#_, bw = cv2.threshold(imgBlur, 200, 210, cv2.THRESH_BINARY)
##imgCanny = cv2.Canny(bw,80,80)

#imgBlank = np.zeros_like(resized)
#imgContour = resized.copy()
#getContours(bw)
    
#imgStack = stackImages(0.6, ([resized,imgGray,imgBlur],
#                                 [bw,imgContour,imgBlank]))
    
    

#cv2.imshow("Stack", imgStack)
 
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
    _,frameBW = cv2.threshold(frameBlur, 110, 210, cv2.THRESH_BINARY)
    
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