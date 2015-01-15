import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *
import cv2
import numpy as np
import imageshow
import getsquare
import random
import math

maxptsall = []
image = sys.argv[1]
def show():
	originalimg = cv2.imread(image)
	for maxpts in maxptsall:
		img2 = cv2.polylines(originalimg,[np.array(maxpts[0])],True, 255,2)
	cv2.imshow('img2',img2)
	k = cv2.waitKey(0)
	cv2.destroyAllWindows()

def save(name):
	originalimg = cv2.imread(image)
	for maxpts in maxptsall:
		img2 = cv2.polylines(originalimg,[np.array(maxpts[0])],True, 255,2)
	cv2.imwrite(name + ".jpg", img2)

def findborder(ret, maxmin):
	rawmax,columnmax,rawmin,columnmin = maxmin[0],maxmin[1],maxmin[2],maxmin[3]
	pts = cv2.boxPoints(ret)
	pts = np.int0(pts)
	for ptss in pts:
		#print rawmax, rawmin
		if ptss[0] > rawmax:
			rawmax = ptss[0]
		if ptss[0] < rawmin:
			rawmin = ptss[0]
		if ptss[1] > columnmax:
			columnmax = ptss[1]
		if ptss[1] < columnmin:
			columnmin = ptss[1]
	# print pts
	maxpts = [[rawmin, columnmin], [rawmax, columnmin], [rawmax, columnmax], [rawmin, columnmax]]
	maxmin = [rawmax, columnmax, rawmin, columnmin]
	return maxpts, maxmin

def strike(rec1, rec2):
	rawmax,columnmax,rawmin,columnmin = rec1[1][0],rec1[1][1],rec1[1][2],rec1[1][3]
	trackrec = [[columnmin,rawmin], [columnmin,rawmax], [columnmax,rawmin], [columnmax,rawmax]]
	for border in trackrec:
		if border[0] in xrange(rec2[1][3], rec2[1][1]) and border[1] in xrange(rec2[1][2], rec2[1][0]):
			#print border, " in ", rec2[1]
			#if (abs((rec2[1][1]-border[0])*(border[1]-rec2[1][2]))/float(abs(rec2[1][1]-rec2[1][3])*(rec2[1][0]-rec2[1][2]))) > 0.1:
			return 1
	return 0
def merge(rec1, rec2):
	if rec1 in maxptsall and rec2 in maxptsall:
		print "Merge!"
		maxptsall.remove(rec1)
		maxptsall.remove(rec2)
		rawmax1,columnmax1,rawmin1,columnmin1 = rec1[1][0],rec1[1][1],rec1[1][2],rec1[1][3]
		rawmax2,columnmax2,rawmin2,columnmin2 = rec2[1][0],rec2[1][1],rec2[1][2],rec2[1][3]
		rawmax = max(rawmax1, rawmax2)
		rawmin = min(rawmin1, rawmin2)
		columnmax = max(columnmax1, columnmax2)
		columnmin = min(columnmin1, columnmin2)
		trackrec = [[rawmin,columnmin], [rawmax,columnmin], [rawmax,columnmax], [rawmin,columnmax]]
		newrec = [trackrec,[rawmax,columnmax,rawmin,columnmin]]
		#print newrec[1]
		maxptsall.append(newrec)
	return

img = cv2.imread(image, 0)
originalimg = cv2.imread(image)
labels = []
values = []
k = 8

f = open("values", "r")
lines = f.readlines()
vv = lines[0].split(" ")
f = open("labels", "r")
lines = f.readlines()
ll = lines[0].split(" ")
for lll in ll:
	lll = lll[0:len(lll)]
	if lll != "":
		labels.append(float(lll))

validposition = []

for l in labels:
	v = 1 / (1+math.exp(l))
	values.append(v)	

val = np.zeros((img.shape[0]-(k+1), img.shape[1]-(k+1)))
count = 0
for i in xrange(k, img.shape[0]-(k+1)):
	for j in xrange(k, img.shape[1]-(k+1)):
		val[i][j] = values[count]
		if labels[count] == 1.0:
			img[i][j] = 0
			validposition.append([i,j])
		count = count + 1

# do cam shift
# setup initial location of window
count = 0
first = 1
maxmin = [-1, -1, 9999999, 9999999]
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
for vpos in validposition:
	count = count + 1
	if count != 20:
		continue
	else:
		count = 0
	c = vpos[1]
	r = vpos[0]
	w = 5
	h = 5
	track_window = (c,r,w,h)
	# dst = cv2.calcBackProject([val],[0],roi_hist,[0,180],1)
	ret, track_window = cv2.CamShift(val, track_window, term_crit)
	# print "(c,r,w,h) = ", track_window
	x,y,w,h = track_window
	# New Search Window
	maxmin = [-1, -1, 9999999, 9999999]
	tmaxpt, maxmin = findborder(ret, maxmin)
	maxptsall.append([tmaxpt, maxmin])
	originalimg = cv2.imread(image)
#show()
save(image + "cam")

#Merge
for i in xrange(0, 20):
	for pts1 in maxptsall:
		for pts2 in maxptsall:
			if pts2 != pts1:
				if strike(pts1, pts2):
					# print "pts1 = ", pts1
					# print "pts2 = ", pts2
					merge(pts1, pts2)

print "Number of Square = ", len(maxptsall)
show()
i = 0
for maxpts in maxptsall:
	#print maxpts
	i = i + 1
	img2 = cv2.polylines(originalimg,[np.array(maxpts[0])],True, 255,2)
	print maxpts[0]
	rawmax,columnmax,rawmin,columnmin = maxpts[0][1][0],maxpts[0][2][1],maxpts[0][0][0],maxpts[0][0][1]
	originalimg = cv2.imread(image)
	imgsquare = originalimg[columnmin:columnmax, rawmin:rawmax]
	#print imgsquare
	cv2.imwrite(image + "piece" + str(i) + ".jpg", imgsquare)
save(image + "merge")