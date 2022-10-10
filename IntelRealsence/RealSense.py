#############################################
### autor: Lars Hartman                   ###
#############################################

from imports import *

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

        maxDistMeters = 1.63  # [m]
        maxDist = maxDistMeters / depthScale

        align_to = rs.stream.color
        align = rs.align(align_to)

        cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
        cv.waitKey(500)
        return True
    except Exception:
        print("could not open Intel RealSense:")
        traceback.print_exc()
        return False


def getCoords():
    frames = pipeline.wait_for_frames()


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

    gray = cv.cvtColor(bgRemoved, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    _, bw = cv.threshold(gray, 96, 255, cv.THRESH_BINARY)
    contours = cv.findContours(bw, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    cv.imshow('RealSense', bw)
    cv.waitKey(0)
    cont = contours[0]
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

        output = f"R1 X{cX} Y{cY} A{format(angle,'.2f')} O{1 if orientatie else 0}"
        cv.imshow('RealSense', colorImage)
        cv.waitKey(1)

    return output


def exit():
    cv.destroyAllWindows()
    pipeline.stop()
