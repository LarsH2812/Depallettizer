#############################################
### autor: Lars Hartman                   ###
#############################################

import socket as tcp
from time import sleep
from math import sin, cos, radians
from time import sleep
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from cv2 import aruco
import imutils
import traceback

cal_x = {
    0:  -768.14,
    1:  -1.5348,
    2:  -0.0008,
    3:  +1e-6,

    }
cal_y = {
    0:  +1047.9,
    1:  -1.7171,
    2:  -4e-5,
    3:  +2e-8,
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
        framesize = {'width': 1280, 'height': 720}

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

        config.enable_stream(
            rs.stream.depth, framesize["width"], framesize["height"], rs.format.z16, 30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            config.enable_stream(rs.stream.color, framesize["width"], framesize["height"], rs.format.bgr8, 30)

        profile = pipeline.start(config)

        depthSensor = profile.get_device().first_depth_sensor()
        depthScale = depthSensor.get_depth_scale()
        print(f"Depth Scale is: {depthScale}")

        maxDistMeters = 1.83  # [m]
        maxDist = maxDistMeters / depthScale

        align_to = rs.stream.color
        align = rs.align(align_to)

        # cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
        cv.waitKey(1000)
        return True
    except Exception:
        print("could not open Intel RealSense:")
        traceback.print_exc()
        return False


def getCoords():
    frames = pipeline.wait_for_frames()
    output = ""

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
    # cv.imshow('test', bgRemoved)
    gray = cv.cvtColor(bgRemoved, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    _, bw = cv.threshold(gray, 96, 255, cv.THRESH_BINARY)
    contours = cv.findContours(bw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    for cont in contours:
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
            angle = angle + 90

        if 40000 <= area and area <= 90000:
            orientatie = False
        elif 90000 <= area:
            orientatie = True

        if area >= 40000:
            cv.drawContours(colorImage, [box], -1, (255, 255, 255), 2, cv.LINE_AA)
            cv.circle(colorImage, (cX, cY), 7, (255, 255, 255), -1)
            cv.putText(colorImage, f"CENTER:", (cX-20, cY+20),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"({cX}, {cY})", (cX-20, cY+40),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"({format(angle, '.2f')})", (cX-20,
                    cY+60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv.putText(colorImage, f"{orientatie}", (cX-20, cY+80),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            lenArrow = 100
            cv.arrowedLine(colorImage, (cX, cY), (int(cX + lenArrow*cos(radians(angle-90))),
                        int(cY + lenArrow*sin(radians(angle-90)))), (255, 255, 255), 2)
            robX, robY = convert(cY, cX)
            output = f"R1 X{robX} Y{robY} A{format(angle,'.2f')} O{1 if orientatie else 0}"
    # cv.imshow('RealSense', colorImage)
    cv.waitKey(1)

    return output


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
        print(getCoords())
        if cv.waitKey(1) == 27:
            break
    exit()

