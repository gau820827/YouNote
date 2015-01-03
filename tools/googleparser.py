# -*- coding: utf-8 -*-
import urllib2
import re
import sys
import json
from subprocess import call

print "Chinese target is not available now."
print "Enter the target you want to search:"
name = raw_input()
print "Enter the number you want to fetch:"
data = raw_input()
number_of_picture = -1
for time in xrange(0, int(data)):
	start = time*8
	url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
	       'v=1.0&q=' + name + '&userip=INSERT-USER-IP&rsz=8&start=' + str(start))
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	# Process the JSON string.
	results = json.load(response)
	#print results
	for count in xrange(0,8):
		number_of_picture = number_of_picture + 1
		target = results['responseData']['results'][count]['url']
		if ".jpg" in target:
			filename = str(number_of_picture) + "p.jpg"
		else:
			filename = str(number_of_picture) + "p.png"
		try:
			req = urllib2.urlopen(target,timeout=10).read()
			picture = open(filename, "wb")
			picture.write(req)
			picture.close()
			print "Download " + target
		except:
			number_of_picture = number_of_picture-1
			print "Download " + target + " fail!"