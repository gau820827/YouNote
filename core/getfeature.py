from os import listdir
import numpy as np
import random
import cv2
import imageshow
import getsquare

Data = open("Features.train", "w")
#Get (2K+1)*(2K+1) square
k = 3
def GetFeature(datalist, label):
	for data in datalist:
		if label == "1.0":
			img = cv2.imread("./image/text/" + data, 0)
		else:
			img = cv2.imread("./image/non-text/" + data, 0)
		img = cv2.resize(img, (32,32), fx=0.5, fy=0.5)
		print "Size of " + data + ": " + str(img.shape)
		if (img.shape[0] < (2*k+1)) or (img.shape[1] < (2*k+1)):
			continue
		square = []
		for i in xrange(0,20):
			value = []
			a = img.shape[0]-(k+1)
			b = img.shape[1]-(k+1)
			point = [random.randint(min(k,a), max(k,a)), random.randint(min(k,b), max(k,b))]
			for p in getsquare.getSquare(point, k):
				value.append(img[p[0], p[1]])
			value.append(label)
			for j in xrange(0, len(value)):
				v = value[j]
				if j != len(value)-1:
					v = int(v)/1.0
				#print v
				Data.write(str(v) + " ")
				if j == (len(value)-1):
					Data.write('\n')
			square.append(getsquare.getSquare(point, k))
		#imageshow.TestImage(square, img)

TextImage = listdir("./image/text")
NonTextImage = listdir("./image/non-text")
GetFeature(TextImage, "1.0")
GetFeature(NonTextImage, "-1.0")