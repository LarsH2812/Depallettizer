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
from IntelRealsence import RealSense
from labeldetectie import labels


PCHOSTNAME = tcp.gethostname()
HOSTIP = tcp.gethostbyname(PCHOSTNAME)
HOSTPORT = 42523
SERVERADRESS = (HOSTIP, HOSTPORT)

robotIp = "198.162.0.5"


def init():
    ret1 = RealSense.init()
    ret2 = labels.init()

    if not (ret1 and ret2):
        print('[*] could not open one of the cams')
        exit(0)


if __name__ != "__main__":

    init()

    print(f"""
    pc name:    {PCHOSTNAME},
    ip address: {HOSTIP},
    pc port:    {HOSTPORT}
    """)

    tcpSocket = tcp.socket(tcp.AF_INET, tcp.SOCK_STREAM)
    tcpSocket.bind(SERVERADRESS)
    tcpSocket.listen(5)

    while True:
        print(
            f"\u001b[34m [*] \u001b[0m Started listening on :{HOSTIP}:{HOSTPORT}")
        clientSocket, (clientAddress, clientPort) = tcpSocket.accept()

        print(
            f"\u001b[34m [*] \u001b[0m Got connection from {clientAddress}:{clientPort}")

        while True:
            request = clientSocket.recv(1024).decode()
            if request == 'Q1':
                coords = RealSense.getCoords()
                print(coords)
                clientSocket.send(coords.encode())
            elif request == 'Q2':
                label = labels.getLabel()
                print(label)
                clientSocket.send(label.encode())
            elif request == 'close':
                break
            elif request == 'quit':
                break
        if request == 'quit':
            break
        clientSocket.close()
    RealSense.exit()
else:
    init()
    while True:
        command = input(">>>")
        if command == "Q1":
            print(RealSense.getCoords())
        elif command == "Q2":
            print(labels.getLabel())
        elif command.lower() == "stop":
            break
