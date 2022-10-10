from imports import *
from IntelRealsence import RealSense

def init():
    ret = RealSense.init()
    if not ret:
        exit(0)



if __name__ == "__main__":

    init()

    while True:
        request = input("show me what you got!\n>>>")
        if request == 'Q1':
            coords = RealSense.getCoords()
            print(coords)
        else: 
            break
    
    RealSense.exit()
