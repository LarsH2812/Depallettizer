import cv2 as cv
import numpy as np
import time

boxes = cv.imread("boxes.png")
cv.imshow('boxes',  boxes)

gray = cv.cvtColor(boxes, cv.COLOR_BGR2GRAY)

_, bw = cv.threshold(gray, 105, 255, cv.THRESH_BINARY_INV)

contrours, hierarchy = cv.findContours(bw, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

cv.drawContours(boxes, contrours, -1,(255,0,0), 2,cv.LINE_AA )


cv.imshow('gray',   gray )
cv.imshow('bw',     bw   )
cv.imshow('out',    boxes)



cv.waitKey(0)