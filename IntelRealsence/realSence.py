#############################################
### autor: Lars Hartman                   ###
#############################################

from math import sin, cos, radians
from time import sleep
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
from cv2 import aruco
import imutils


cnts = None

framesize = {'width':1280, 'height': 720}

ARUCO_DICT = {
	"DICT_4X4_50":          aruco.DICT_4X4_50,
	"DICT_4X4_100":         aruco.DICT_4X4_100,
	"DICT_4X4_250":         aruco.DICT_4X4_250,
	"DICT_4X4_1000":        aruco.DICT_4X4_1000,
	"DICT_5X5_50":          aruco.DICT_5X5_50,
	"DICT_5X5_100":         aruco.DICT_5X5_100,
	"DICT_5X5_250":         aruco.DICT_5X5_250,
	"DICT_5X5_1000":        aruco.DICT_5X5_1000,
	"DICT_6X6_50":          aruco.DICT_6X6_50,
	"DICT_6X6_100":         aruco.DICT_6X6_100,
	"DICT_6X6_250":         aruco.DICT_6X6_250,
	"DICT_6X6_1000":        aruco.DICT_6X6_1000,
	"DICT_7X7_50":          aruco.DICT_7X7_50,
	"DICT_7X7_100":         aruco.DICT_7X7_100,
	"DICT_7X7_250":         aruco.DICT_7X7_250,
	"DICT_7X7_1000":        aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL":  aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5":   aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9":   aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10":  aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11":  aruco.DICT_APRILTAG_36h11
}

arucoDict = aruco.Dictionary_get(ARUCO_DICT["DICT_ARUCO_ORIGINAL"])
arucoParams = aruco.DetectorParameters_create()
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# videocapture = cv.VideoWriter("ContourDetected.avi",  cv.VideoWriter_fourcc('M','J','P','G'), 30, (1280,960))

# Get device product line for setting a supporting resolution
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
    exit(0)

config.enable_stream(rs.stream.depth, framesize["width"], framesize["height"], rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, framesize["width"], framesize["height"], rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

depthSensor = profile.get_device().first_depth_sensor()
depthScale  = depthSensor.get_depth_scale()
print(f"Depth Scale is: {depthScale}")

maxDistMeters = 1.63 #[m]


align_to = rs.stream.color
align = rs.align(align_to)

cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)

def getFrame(Dist = 0):
    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)

    alignedDepthFrame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    if not alignedDepthFrame or not color_frame:
        return

    depthImage = np.asanyarray(alignedDepthFrame.get_data())
    colorImage = np.asanyarray(color_frame.get_data())

    depthImage3D = np.dstack((depthImage,depthImage,depthImage))
    if not Dist <= 0:
        maxDist = maxDistMeters / depthScale
        bgRemoved = np.where((depthImage3D > maxDist) | (depthImage3D <= 0), 0, colorImage)
        return bgRemoved
    else:
        return colorImage

def translateCoords(coord):
    x = coord[0]
    y = coord[1]
    outX = 1e-6*x**3 - 0.0008*x**2 - 1.5348*x - 768.14
    outY = 2e-8*y**3 - 4e-5*y**2 - 1.7171*y + 1047.9
    return outX, outY
try:
    while True:

        k = cv.waitKey(1)

        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite("boxes.png",bgRemoved)
        elif k == ord('+'):
            maxDistMeters = maxDistMeters + 0.01
            print(maxDistMeters)
        elif k == ord('-'):
            maxDistMeters = maxDistMeters - 0.01
            print(maxDistMeters)
        elif True:
            frame = getFrame()
            (corners, ids, rejected) = aruco.detectMarkers(frame, arucoDict, parameters= arucoParams)

            if not ids is None:
                ids = ids.flatten()
                cX = 0
                cY = 0

                for (markerCorners, markerID) in zip(corners, ids):
                    (topLeft, topRight, bottomRight, bottomLeft) = markerCorners.reshape((4,2))
                    
                    topRight = (int(topRight[0]), int(topRight[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    topCenter = (int((topRight[0]+topLeft[0])/2), int((topRight[1]+topLeft[1])/2))

                    cX = cX+int((topRight[1] + bottomLeft[1]) / 2)
                    cY = cY+int((topRight[0] + bottomLeft[0]) / 2)

                    h = bottomRight[1] - topRight[1]
                    w = topRight[0] - topLeft[0]
                    
                cX = int(cX / len(ids))
                cY = int(cY / len(ids))
                cv.circle(frame, (cY,cX), 5, (255,0,0), -1, cv.LINE_AA)
                cv.putText(frame, f"{cX}, {cY}", (cY-65, cX), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), lineType=cv.LINE_AA )

            
            cv.imshow("RealSense", frame)
                

            if k == ord('q'):
                pX, pY = translateCoords((cX, cY))
                print(f"({pX}, \t{pY})")
        elif k == 32 :
            
            

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()

            aligned_frames = align.process(frames)

            alignedDepthFrame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            if not alignedDepthFrame or not color_frame:
                continue

            depthImage = np.asanyarray(alignedDepthFrame.get_data())
            colorImage = np.asanyarray(color_frame.get_data())

            depthImage3D = np.dstack((depthImage,depthImage,depthImage))
            if not maxDistMeters <= 0:
                maxDist = maxDistMeters / depthScale
                bgRemoved = np.where((depthImage3D > maxDist) | (depthImage3D <= 0), 0, colorImage)

            depthColormap = cv.applyColorMap(cv.convertScaleAbs(depthImage, alpha=0.03), cv.COLORMAP_JET)
            horizontal1 = np.hstack((depthColormap,colorImage, bgRemoved))
            # Show images
            

            # cv.imshow('RealSense', bgRemoved)

            gray = cv.cvtColor(bgRemoved, cv.COLOR_BGR2GRAY)
            gray = cv.GaussianBlur(gray, (5,5), 0)
            _, bw = cv.threshold(gray, 96, 255, cv.THRESH_BINARY)
            contours = cv.findContours(bw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            for cont in contours:
                try:
            
                    M = cv.moments(cont)
                    area = M["m00"]

                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

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
                        cv.drawContours(colorImage, [box], -1, (255,255,255), 2, cv.LINE_AA)
                        cv.circle(colorImage, (cX,cY), 7, (255,255,255), -1)
                        cv.putText(colorImage, f"CENTER:", (cX-20,cY+20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
                        cv.putText(colorImage, f"({cX}, {cY})", (cX-20,cY+40),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
                        cv.putText(colorImage, f"({format(angle, '.2f')})", (cX-20,cY+60),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
                        cv.putText(colorImage, f"{orientatie}", (cX-20,cY+80),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)

                        lenArrow = 100
                        cv.arrowedLine(colorImage, (cX,cY), (int(cX + lenArrow*cos(radians(angle-90))), int(cY + lenArrow*sin(radians(angle-90)))), (255,255,255), 2)

                        output = [(cX, cY,angle), (area,orientatie)]

                        

                except:
                    cv.drawContours(colorImage,[cont],-1,(0,0,255), 2)

            horizontal2 = np.hstack((np.dstack((gray,gray,gray)),np.dstack((bw,bw,bw)), colorImage))
            images = np.vstack((horizontal1,horizontal2))
            
            # output = np.array(output)
            cv.imshow('RealSense', bgRemoved)
            # print(output)
            # videocapture.write(images)

finally:
    # Stop streaming
    cv.destroyAllWindows()
    pipeline.stop()