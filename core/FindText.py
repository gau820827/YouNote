import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *
import cv2
import numpy as np
import imageshow
import getsquare

img = cv2.imread("./test.jpg", 0)
#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
m = svm_load_model('model_file')
labels = []
target = []
for i in xrange(3, img.shape[0]-4):
	for j in xrange(3, img.shape[1]-4):
		target.append([i,j])
		value = [[]]
		y = [0]
		for p in getsquare.getSquare([i,j]):
			value[0].append(img[p[0], p[1]])
		p_labs, p_acc, p_vals = svm_predict(y, value, m)
		labels.append(p_labs[0])
#print labels
for i in xrange(0, len(target)):
	if labels[i] == 1.0:
		img[target[i][0], target[i][1]] = 0
imageshow.ShowImage(img)