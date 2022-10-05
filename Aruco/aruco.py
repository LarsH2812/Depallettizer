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

img = cv.imread("Aruco/WIN_20221005_12_40_15_Pro.jpg")
cv.imshow('Input', img)
cv.waitKey(0)