import sys
sys.path.insert(0, "./libsvm-3.20/python")
from svmutil import *
from svm import *

import numpy as np
import math
import random

def readfile(f):
	y = []
	x = []
	for lines in f.readlines():
		xx = []
		line = lines.split(" ")
		line.remove("\n")
		for data in line:
			if data == "1.0" or data == "-1.0":
				y.append(float(data))
			else:
				xx.append(float(data))
		x.append(xx)
	return y, x

f = open('./Features.train', 'r')
y, x = readfile(f)
tmp = zip(y, x)
random.shuffle(tmp)
for i in xrange(len(x)):
	y[i] = tmp[i][0]
	x[i] = tmp[i][1]
gamma = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
C = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
maximum = 0
for g in gamma:
	for c in C:
		parameter = '-t 2 -c ' + str(c) + ' -q -g ' + str(g)
		prob = svm_problem(y[100:], x[100:])
		param = svm_parameter(parameter)
		m = svm_train(prob, param)
		p_labs, p_acc, p_vals = svm_predict(y[:99], x[:99], m)
		if p_acc > maximum:
			bestmodel = m
svm_save_model('model_file', bestmodel)