import cv2 as cv
import cv2.aruco as aruco 

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

vid = cv.VideoCapture(0,cv.CAP_DSHOW)

vid.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 1280)

writer = cv.VideoWriter("ArUco.avi",  cv.VideoWriter_fourcc('M','J','P','G'), 30, (1280,720))
capturing = False

arucoDict = aruco.Dictionary_get(ARUCO_DICT["DICT_ARUCO_ORIGINAL"])
arucoParams = aruco.DetectorParameters_create()

cv.namedWindow("output",cv.WINDOW_AUTOSIZE)
k = cv.waitKey(1)

while (k != 27):
	_, frame = vid.read()
	(corners, ids, rejected) = aruco.detectMarkers(frame,arucoDict, parameters = arucoParams) 
	if not ids is None:
		ids = ids.flatten()

		for (marekerCorner, markerID) in zip(corners, ids):
			(topLeft, topRight, bottomRight, bottomLeft) = marekerCorner.reshape((4,2))

			topRight = (int(topRight[0]), int(topRight[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			topCenter = (int((topRight[0]+topLeft[0])/2), int((topRight[1]+topLeft[1])/2))

			cX = int((topRight[0] + bottomLeft[0]) / 2)
			cY = int((topRight[1] + bottomLeft[1]) / 2)

			h = bottomRight[1] - topRight[1]
			w = topRight[0] - topLeft[0]  

			cv.line(frame, topRight, topLeft, (0,255,0), 1, cv.LINE_AA)
			cv.line(frame, topLeft, bottomLeft, (0,255,0), 1, cv.LINE_AA)
			cv.line(frame, bottomLeft, bottomRight, (0,255,0), 1, cv.LINE_AA)
			cv.line(frame, bottomRight, topRight, (0,255,0), 1, cv.LINE_AA)
			cv.putText(frame,f"ID: {markerID}", (cX+20, cY+20),cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,0), 1, cv.LINE_AA)
			# cv.putText(frame, f"Height = {h}",(cX +int(w/2), cY),cv.FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 1, cv.LINE_AA)
			# cv.putText(frame, f"Width = {w}",(cX-int(w/2) , cY+int(h/2)),cv.FONT_HERSHEY_SIMPLEX, 1,(0,255,0), 1, cv.LINE_AA)
			cv.arrowedLine(frame, (cX, cY), topCenter, (0,255,0),1,cv.LINE_AA)

			cv.circle(frame, (cX, cY),5,(0,255,0),-1,cv.LINE_AA)
	
	if capturing:
		writer.write(frame)
		cv.putText(frame, "Caputuring!", (20,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),1,cv.LINE_AA)
	cv.imshow("output",frame)
	k = cv.waitKey(1)
	if k == 32:
		capturing = True if not capturing else False


cv.destroyAllWindows()
vid.release()
