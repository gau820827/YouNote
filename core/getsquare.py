def getSquare(point):
	square = []
	for i in xrange(0,7):
		if i < 3:
			for j in xrange(0,3):
				square.append([point[0]-3+i, point[1]-3+i+(3-i)*j])
		elif i == 3:
			for j in xrange(0,7):
				square.append([point[0]-3+i, point[1]-3+j])
		elif i > 3:
			for j in xrange(0,3):
				square.append([point[0]-3+i, point[1]+3-i+(i-3)*j])
	return square