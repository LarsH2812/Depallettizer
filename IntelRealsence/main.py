## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2 as cv

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

videocapture = cv.VideoWriter("ContourDetected.avi",  cv.VideoWriter_fourcc('M','J','P','G'), 30, (1280,960))

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

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

depthSensor = profile.get_device().first_depth_sensor()
depthScale  = depthSensor.get_depth_scale()
print(f"Depth Scale is: {depthScale}")

maxDistMeters = 1.65 #[m]
maxDist = maxDistMeters / depthScale

align_to = rs.stream.color
align = rs.align(align_to)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        aligned_frames = align.process(frames)

        alignedDepthFrame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not alignedDepthFrame or not color_frame:
            continue

        depthImage = np.asanyarray(alignedDepthFrame.get_data())
        colorImage = np.asanyarray(color_frame.get_data())

        gray_color = 0
        white_color = 0
        depthImage3D = np.dstack((depthImage,depthImage,depthImage))
        bgRemoved = np.where((depthImage3D > maxDist) | (depthImage3D <= 0), gray_color, colorImage)

        depthColormap = cv.applyColorMap(cv.convertScaleAbs(depthImage, alpha=0.03), cv.COLORMAP_JET)

        # Show images
        cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)

        # cv.imshow('RealSense', bgRemoved)

        gray = cv.cvtColor(bgRemoved, cv.COLOR_BGR2GRAY)
        horizontal1 = np.hstack((bgRemoved,np.dstack((gray,gray,gray))))
        _, bw = cv.threshold(gray, 105, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(bw, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        cv.drawContours(bgRemoved, contours, -1, (0,255,0), 2, cv.LINE_AA)
        horizontal2 = np.hstack((np.dstack((bw,bw,bw)), bgRemoved))
        images = np.vstack((horizontal1,horizontal2))
        
        cv.imshow('RealSense', images)
        videocapture.write(images)

        k = cv.waitKey(1)

        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite("boxes.png",bgRemoved)

finally:
    print(images.shape)
    # Stop streaming
    cv.destroyAllWindows()
    pipeline.stop()