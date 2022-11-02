#############################################
### autor: Lars Hartman                   ###
#############################################

import socket as tcp
from time import sleep
from math import dist, sin, cos, radians
from time import sleep
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from cv2 import aruco
import imutils
import traceback
import logging

done = False

cal_x = {
    0: -466.98,
    1: -1.9902,
}
cal_y = {
    0: +910.87,
    1: -1.8597,
}

pipeline = None
align = None
maxDist = None


def init():
    global pipeline
    global align
    global maxDist
    try:
        cnts = None
        framesize = {
            'width': 1280,
            'height': 720}

        pipeline = rs.pipeline()
        config = rs.config()

        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            return False

        config.enable_stream(rs.stream.depth, framesize["width"], framesize["height"], rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, framesize["width"], framesize["height"], rs.format.bgr8, 30)

        profile = pipeline.start(config)

        depthSensor = profile.get_device().first_depth_sensor()
        depthScale = depthSensor.get_depth_scale()
        print(f"Depth Scale is: {depthScale}")

        maxDistMeters = 1.85  # [m]
        maxDist = maxDistMeters / depthScale

        align_to = rs.stream.color
        align = rs.align(align_to)

        cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
        # cv.waitKey(0)
        return True
    except Exception:
        print("could not open Intel RealSense:")
        traceback.print_exc()
        return False


def getCoords():
    outputArray = []
    for i in range(5):
        frames = pipeline.wait_for_frames()
    output = "R0"

    aligned_frames = align.process(frames)

    alignedDepthFrame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    if not alignedDepthFrame or not color_frame:
        return

    depthImage = np.asanyarray(alignedDepthFrame.get_data())
    colorImage = np.asanyarray(color_frame.get_data())

    gray_color = 0
    depthImage3D = np.dstack((depthImage, depthImage, depthImage))
    bgRemoved = np.where((depthImage3D > maxDist) | (depthImage3D <= 0), gray_color, colorImage)
    imrows, imcols = bgRemoved.shape[:2]
    bgCropped = bgRemoved[0:imrows, 150:imcols]
    colorImage = colorImage[0:imrows, 150:imcols]
    depthImage3D = depthImage3D[0:imrows, 150:imcols]
    depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depthImage, alpha=0.03), cv.COLORMAP_JET)[0:imrows, 150:imcols]

    gray = cv.cvtColor(bgCropped, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    _, bw = cv.threshold(gray, 92, 255, cv.THRESH_BINARY)
    bw = cv.GaussianBlur(bw, (23, 23), 0)
    _, bw = cv.threshold(bw, 254, 255, cv.THRESH_BINARY)
    # bw = cv.GaussianBlur(bw, (5, 5), 0)
    # _, bw = cv.threshold(bw, 254, 255, cv.THRESH_BINARY)
    cv.imwrite("bw.png", bw)
    HORIZONTAL1 = np.hstack((colorImage, np.dstack((gray, gray, gray)), np.dstack((bw, bw, bw))))
    contours = cv.findContours(bw, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
    contoured = colorImage.copy()
    cv.drawContours(contoured, contours[0], -1, (255, 0, 0), 2, cv.LINE_AA)
    contours = imutils.grab_contours(contours)

    for cont in contours:
        global done
        M = cv.moments(cont)
        area = M["m00"]
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except Exception:
            pass

        rect = cv.minAreaRect(cont)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        length, width = max(rect[1]), min(rect[1])

        orientatie = ""

        angle = rect[-1]

        if rect[1][0] < rect[1][1]:
            angle = angle
        else:
            angle = angle+90

        if 0 <= (width) and (width) <= 130:
            orientatie = False
        elif 135 <= (width):
            orientatie = True

        if 35000 <= area and area <= 80000:
            robX, robY = convert(cY, cX)
            radius = dist((0, 0), (robX, robY))

            cv.drawContours(colorImage, [box], -1,(255, 255, 255), 2, cv.LINE_AA)
            cv.circle(colorImage, (cX, cY), 7, (255, 255, 255), -1)
            cv.putText(colorImage, f"CENTER:", (cX-20, cY+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"({format(robX,'.3f')}, {format(robY,'.3f')})", (cX-20, cY+40),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"({format(angle, '.2f')})", (cX-20,cY+60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"{orientatie}", (cX-20, cY+80),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"width: {width}", (cX-20, cY+100),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"inrange: {True if radius < 1550 else False}", (cX-20, cY-20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            lenArrow = 100
            cv.arrowedLine(colorImage, (cX, cY), (int(cX + lenArrow*cos(radians(angle-90))),int(cY + lenArrow*sin(radians(angle-90)))), (255, 255, 255), 2)

            output = f"R1 X{format(robX,'.3f')} Y{format(robY,'.3f')} A{format(angle-90,'.2f')} O{1 if orientatie else 0}"
            if radius < 1520:
                print(radius)
                outputArray.append([cX, output])
            #output = f"R1 X{cY} Y{cX} A{format(angle,'.2f')} O{1 if orientatie else 0}"

    HORIZONTAL2 = np.hstack((bgCropped, contoured, colorImage))
    total = np.vstack((HORIZONTAL1, HORIZONTAL2))
    if not done:
        done = cv.imwrite('video.tiff', total)
    total = cv.resize(total, None, fx=0.5, fy=0.5,interpolation=cv.INTER_LINEAR)
    cv.imshow('RealSense', total)
    cv.waitKey(1)
    if len(outputArray) == 0:

        return "R0"
    else:
        outputArray.sort()
        return outputArray[0][1]


def exit():
    cv.destroyAllWindows()
    pipeline.stop()


def convert(X, Y):
    outX, outY = 0, 0
    for i in range(len(cal_x)):
        outX = outX + cal_x[i]*X**i
    for j in range(len(cal_y)):
        outY = outY + cal_y[j]*Y**j
    return outX, outY


if __name__ == "__main__":
    init()

    while True:
        out = getCoords()
        print(out)
        k = cv.waitKey(0)
        if k == 27:
            break
    exit()
