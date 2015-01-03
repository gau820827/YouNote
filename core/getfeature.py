from os import listdir
import numpy as np
import random
import cv2
import imageshow
import getsquare

Data = open("Features.train", "w")

def GetFeature(datalist, label):
	for data in datalist:
		if label == "1.0":
			img = cv2.imread("./image/text/" + data, 0)
		else:
			img = cv2.imread("./image/non-text/" + data, 0)
		img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
		print "Size of " + data + ": " + str(img.shape)
		square = []
		for i in xrange(0,20):
			value = []
			point = [random.randint(3, img.shape[0]-4), random.randint(3, img.shape[1]-4)]
			for p in getsquare.getSquare(point):
				value.append(img[p[0], p[1]])
			value.append(label)
			for v in value:
				#print v
				Data.write(str(v) + " ")
				if v == label:
					Data.write('\n')
			square.append(getsquare.getSquare(point))
		#imageshow.TestImage(square, img)

TextImage = listdir("./image/text")
NonTextImage = listdir("./image/non-text")
GetFeature(TextImage, "1.0")
GetFeature(NonTextImage, "-1.0")