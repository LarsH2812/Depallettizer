import cv2
import numpy as np

def empty(a):
   pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print("area",area)
        if area>20000 and area<25000:
            cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 5)
            #peri = cv2.arcLength(cnt,True)
            #print(peri)
            #approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))
            #objCor = len(approx)
            #x, y, w, h = cv2.boundingRect(approx)

            #if objCor ==3: objectType ="Tri"
            #elif objCor == 4:
                #aspRatio = w/float(h)
                #if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
                #else:objectType="Rectangle"
            #elif objCor>4: objectType= "Circles"
            #else:objectType="None"




path = "E:\HBO Werktuigbouwkunde\SMR\images\Zonderlabel.jpeg"
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",9,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",0,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",95,95,empty)
cv2.createTrackbar("Val Min","TrackBars",129,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)


while True:    
   img = cv2.imread(path)
   print("Original Dimensions",img.shape)
   
   #Het schalen van de afbeeldingen
   scale_percent = 20
   Width = int(img.shape[1]*scale_percent/100)
   Height = int(img.shape[0]*scale_percent/100)
   dim = (Width, Height)
    
   resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
   
    #Color Detection
   imgHSV = cv2.cvtColor(resized,cv2.COLOR_BGR2HSV)
   h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
   h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
   s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
   s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
   v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
   v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
   print(h_min,h_max,s_min,s_max,v_min,v_max)
   lower = np.array([h_min,s_min,v_min])
   upper = np.array([h_max,s_max,v_max])
   mask = cv2.inRange(imgHSV,lower,upper)
   imgResult = cv2.bitwise_and(resized,resized,mask=mask)


       
#Contour Detection
#imgGray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
#imgBlur = cv2.GaussianBlur(imgGray,(5,5),0)
#_, bw = cv2.threshold(imgBlur, 200, 210, cv2.THRESH_BINARY)
   imgCanny = cv2.Canny(mask,50,50)

   imgBlank = np.zeros_like(resized)
   imgContour = resized.copy()
   getContours(imgCanny)
    
   imgStack = stackImages(0.6, ([resized,mask,imgHSV],
                                 [imgCanny,imgContour,imgBlank]))
    
    
    
    #cv2.imshow("Original",img)
    #cv2.imshow("HSV",imgHSV)
    #cv2.imshow("mask", mask)
    #cv2.imshow("Result",imgResult)
   cv2.imshow("Stack", imgStack)
   cv2.waitKey(1)
    
    
cv2.waitKey(0)
cv2.destroyAllWindows()