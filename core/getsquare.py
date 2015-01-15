def getSquare(point, k):
	square = []
	for i in xrange(0,2*k+1):
		if i < k:
			for j in xrange(0,3):
				square.append([point[0]-(k)+i, point[1]-(k)+i+((k)-i)*j])
		elif i == k:
			for j in xrange(0,2*k+1):
				square.append([point[0]-(k)+i, point[1]-(k)+j])
		elif i > k:
			for j in xrange(0,3):
				square.append([point[0]-(k)+i, point[1]+(k)-i+(i-(k))*j])
	return square