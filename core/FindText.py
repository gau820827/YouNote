import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *
import cv2
import numpy as np
import imageshow
import getsquare
import random

def washtraining(y, x, img):
	#Get (2K+1)*(2K+1) square
	k = 3
	m = svm_load_model('model_file')
	labels = []
	target = []
	values = []
	for i in xrange(k, img.shape[0]-(k+1), 2*k+1):
		for j in xrange(k, img.shape[1]-(k+1), 2*k+1):
			target.append([i,j])
			value = [[]]
			temp_label = [0]
			for p in getsquare.getSquare([i,j], k):
				value[0].append(img[p[0], p[1]])
			p_labs, p_acc, p_vals = svm_predict(temp_label, value, m)
			labels.append(p_labs[0])
	#Revise training set according to labels
	for i in xrange(0, len(target)):
		xvalues = []
		if labels[i] == 1.0:
			if random.randint(1,100) <= 10:
				square = getsquare.getSquare([target[i][0], target[i][1]], k)
				for point in square:
					xvalues.append(img[point[0], point[1]])
				x.append(xvalues)
				y.append(-1.0)
			else:
				continue
	return y, x