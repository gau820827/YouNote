from os import listdir
import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *

import cv2
import numpy as np
import math
import random
import FindText

def readfile(f):
	y = []
	x = []
	for lines in f.readlines():
		xx = []
		line = lines.split(" ")
		line.remove("\n")
		for i in xrange(0, len(line)):
			data = line[i]
			if i == len(line)-1:
				y.append(float(data))
			else:
				xx.append(float(data))
		x.append(xx)
	return y, x

def train(y, x):
	gamma = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
	C = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
	maximum = 0
	for g in gamma:
		for c in C:
			parameter = '-t 2 -c ' + str(c) + ' -q -g ' + str(g)
			fold = int(len(y)/6.0)
			prob = svm_problem(y[fold+1:], x[fold+1:])
			param = svm_parameter(parameter)
			m = svm_train(prob, param)
			p_labs, p_acc, p_vals = svm_predict(y[:fold], x[:fold], m)
			if p_acc > maximum:
				bestmodel = m
	return bestmodel

def replace(y, x, bestmodel):
	support_vectors = bestmodel.get_SV()
	nonsvlist = []
	sv = 0
	for v in xrange(0, len(y)):
		if y[v] == 1.0:
			continue
		elif y[v] == -1.0:
			for i in xrange(0, len(support_vectors)):
				tmp = support_vectors[i].values()
				tmp.pop()
				#print tmp
				sv = 0
				if x[v] == tmp:
					sv = 1
					#print "SV!!"
					continue
			if sv == 0:
				nonsvlist.append(v)
	for v in nonsvlist:
		y[v] = None
		x[v] = None
	y = [yy for yy in y if yy != None]
	x = [xx for xx in x if xx != None]
	return y, x

f = open('./Features.train', 'r')
y, x = readfile(f)
tmp = zip(y, x)
random.shuffle(tmp)
for i in xrange(len(x)):
	y[i] = tmp[i][0]
	x[i] = tmp[i][1]

#Initial Training
bestmodel = train(y, x)
svm_save_model('model_file', bestmodel)
#Replace Training set with all text and all SV nontext
y, x = replace(y, x, bestmodel)
#Scan all non-text image
NonTextImage = listdir("./image/non-text")
for image in NonTextImage:
	print "Start wash ", image
	img = cv2.imread("./image/non-text/" + image, 0)
	img = cv2.resize(img, (256,256), fx=0.5, fy=0.5)
	#Wash Training Set
	y, x = FindText.washtraining(y, x, img)
	#Finish Wash
	print "New y = ", y, len(y)
	print "New x = ", x, len(x)
	bestmodel = train(y, x)
	svm_save_model('model_file', bestmodel)
	y, x = replace(y, x, bestmodel)
print "===Finalized training!!==="
print "Final y = ", y, len(y)
print "Final x = ", x, len(x)
finalmodel = train(y, x)
svm_save_model('Final_model', finalmodel)