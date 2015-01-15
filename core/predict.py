import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *
import cv2
import numpy as np
import imageshow
import getsquare
import random

image = sys.argv[1]
img = cv2.imread(image, 0)
originalimg = cv2.imread(image)
#img = cv2.resize(img, (256,256))
#Get (2K+1)*(2K+1) square
k = 8
m = svm_load_model("Good_model")
labels = []
target = []
values = []
for i in xrange(k, img.shape[0]-(k+1)):
	for j in xrange(k, img.shape[1]-(k+1)):
		target.append([i,j])
		value = [[]]
		temp_label = [-1]
		for p in getsquare.getSquare([i,j], k):
			value[0].append(float(img[p[0], p[1]]))
		p_labs, p_acc, p_vals = svm_predict(temp_label, value, m)
		labels.append(p_labs[0])
		values.append(p_vals[0])
print len(labels)
print len(values)

f = open("values", "w")
for v in values:
	f.write(str(v) + " ")
f = open("labels", "w")
for l in labels:
	f.write(str(l) + " ")

mini = min(values)
maxi = max(values)
for v in values:
	v[0] = v[0] + (-1*mini[0])
	v[0] = v[0] / maxi[0]
val = np.zeros((img.shape[0]-(k+1), img.shape[1]-(k+1)))
count = 0
for i in xrange(k, img.shape[0]-(k+1)):
	for j in xrange(k, img.shape[1]-(k+1)):
		val[i][j] = values[count][0]
		if labels[count] == 1.0:
			img[i][j] = 0
		count = count + 1
#imageshow.ShowImage(img)
cv2.imwrite(image + "black.jpg", img)