import cv2

def ShowImage(image):
	cv2.imshow('image',image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def TestImage(points, image):
	for p in points:
		for pp in p:
			image[pp[0], pp[1]] = 0
	ShowImage(image)