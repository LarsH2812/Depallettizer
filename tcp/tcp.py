import socket as tcp
from time import sleep
from turtle import width
import cv2 as cv
from cv2 import aruco
from math import sin, cos, radians
from time import sleep
import pyrealsense2 as rs
import numpy as np
import imutils

pcHostName = tcp.gethostname()
hostIp = tcp.gethostbyname(pcHostName)
hostPort = 49252
serverAdress = (hostIp, hostPort)

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
    print("This setup requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, framesize["width"],framesize["height"], rs.format.z16, 30)

config.enable_stream(rs.stream.color, framesize["width"], framesize["height"], rs.format.bgr8, 30)

profile = pipeline.start(config)

depthSensor = profile.get_device().first_depth_sensor()
depthScale = depthSensor.get_depth_scale()
print(f"Depth Scale is: {depthScale}")
maxDistMeters = 1.63 #[m]
maxDist = maxDistMeters / depthScale

align = rs.align(rs.stream.color)

cv.namedWindow('RealSense', cv.WINDOW_AUTOSIZE)
frames = pipeline.wait_for_frames()

aligned_frames = align.process(frames)

depthFrame = aligned_frames.get_depth_frame()
colorFrame = aligned_frames.get_color_frame()

depthImage = np.asanyarray(depthFrame.get_data())
colorImage = np.asanyarray(colorFrame.get_data())

depthImage = np.dstack((depthImage,depthImage,depthImage))
bgRemoved = np.where((depthImage > maxDist) | (depthImage <= 0),0,colorImage)

dephtColormap = cv.applyColorMap(cv.convertScaleAbs(depthImage, alpha = 0.3), cv.COLORMAP_JET)

cv.imshow('RealSense', dephtColormap)
cv.waitKey(1)

def getData(socket):
    data = socket.recv(1024).decode()
    if data is None:
        print("[!] DID NOT RECEIVE DATA, RETRYING")
        data = getData(socket)
        return data
    else:
        print("[*] RECEIVED DATA")
        return data

robotIp = "198.162.0.1"
PORT = 2000 #todo: change this

print(f"""
pc name:    {pcHostName},
ip address: {hostIp},
pc port:    {hostPort}
""")

tcpSocket = tcp.socket(tcp.AF_INET, tcp.SOCK_STREAM)
tcpSocket.bind(serverAdress)
tcpSocket.listen(5)

x = 5.454
y = 1231.858
rot = 90
ori = 0

while True:
    print(f"[*] Started listening on :{hostIp}:{hostPort}")
    clientSocket, clientAddress = tcpSocket.accept()

    print(f"[*] Got connection from {clientAddress[0]}:{clientAddress[1]}")

    # while True:
    #     data = clientSocket.recv(1024).decode()
    #     print(f"[*] Received {data} from the client")
    #     print("[*] Processing data")
    #     if(data == "hello server"):
    #         clientSocket.send("1".encode())
    #         print("[*] Reply sent: 1")
    #     elif(data=="close"):
    #         clientSocket.send("Goodbye".encode())
    #         print("[*] Reply sent: Goodbye")
    #         print("[*] Connection closed.")
    #         clientSocket.close()
    #         break
    #     elif(data == "quit"):
    #         clientSocket.send("Server stopped".encode())
    #         print("[*] Reply sent: Server Stopped")
    #         clientSocket.close()
    #         break
    #     elif(data=="getData"):
    #         coords = f"{x},{y},{rot},{ori}"
    #         print(coords)
    #         clientSocket.send(coords.encode())
    #         print(f"[*] Reply sent: {coords}")

    if clientAddress == robotIp:
        print(f"[*] CONNECTED TO KAWASAKI AT {clientAddress[0]}")
        print(f"[*] SENDING ROBOT TO FIRST POSITION")
        clientSocket.send("1")
        sleep(3)
        data = getData(clientSocket)
        print(f"[*] Processing data")


print("[*] End of server program")