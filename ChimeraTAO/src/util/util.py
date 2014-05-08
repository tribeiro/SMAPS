
import struct
import numpy as np
import _skysub

####################################################################################################################################

def readtarget(filename):

	'''
	Read a formated target.txt file from TAO.
	'''

	data = []
	fp = open(filename,'r')
	for _data in fp.readlines():
		if len(_data) >= 140:
			data.append(struct.unpack('1sx12sx5sx5sx5s5x6sx5s2x5s3x5s5x5s4x8s3x10sx5s3x16sx4sx10s',_data[:140]))
	fp.close()
	return data

####################################################################################################################################

def readshoot(filename):

	'''
	Read a formated shoot file from TAO.
	'''

	data = []
	fp = open(filename,'r')
	for _data in fp.readlines():
		if len(_data) >= 128:
			data.append(struct.unpack('10sx13sx13sx3sx7sx9sx2sx11sx13sx13s25s',_data[:128]))
	fp.close()
	return data

####################################################################################################################################

def hex2float(istr):

	coords = istr.split(' ')
	
	rval = 0
	firstVal = 0
	for i in range(len(coords)):
		if len(coords[i]) > 0:
			rval += float(coords[i])/60.**firstVal
			firstVal+=1
	return rval

####################################################################################################################################

def prepareDummyRequest(line):
	'''
	Give one line from targets.txt file and it will give a formated request back.
	'''

	reqStr = ''
	#work on object name

	objname = line[1]
	# deleting blanck lines at the end
	nblank = 0
	for i in objname[::-1]:
		if i == ' ':
			nblank+=1
		else:
			break

	#reqStr += objname[:len(objname)-nblank] + ';'

	#for i in range(nfilters):
	#	reqStr += objname[:len(objname)-nblank] + '; 1i; filter=' + filters[i] +'\n'
	user = sciUser
	if line[0] == stdFlag:
		user = stdUser
	reqStr += objname[:len(objname)-nblank] + '; %s 1i exp=600 alt>30 opt\n'%(user)

	return reqStr

####################################################################################################################################

def prepareRequest(line):
	'''
	Give one line from targets.txt file and it will give a formated request back.
	'''

	reqStr = ''
	#work on object name

	objname = line[2]
	# deleting blanck lines at the end
	nblank = 0
	for i in objname[::-1]:
		if i == ' ':
			nblank+=1
		else:
			break

	#reqStr += objname[:len(objname)-nblank] + ';'

	for i in range(nfilters):
		reqStr += objname[:len(objname)-nblank] + '; 1i exp=600 alt>30 opt filter=%s\n'%(filters[i])
	#reqStr += objname[:len(objname)-nblank] + '; 1i; exp=600; alt>30; opt; filter=%s\n'%(filters[0])

	return reqStr

####################################################################################################################################

def getTargets(T0,T1,RA,DEC,mask,texp,sitelat,sitelong):

	obsmask = mask
	
	tbin = 0
	
	ra = RA[obsmask]
	dec = DEC[obsmask]
	mm = obsmask[obsmask]
	targets = np.zeros(len(np.arange(T0,T1,texp)))
	xaxis = np.arange(len(RA))[obsmask]
	
	# Rejecting objects that are close to the moon
	
	for time in np.arange(T0,T1,texp):

		ra = RA[obsmask]
		dec = DEC[obsmask]
		xaxis = np.arange(len(RA))[obsmask]
		
		lst = _skysub.lst(time,sitelong) #*360./24.
		ha = lst - ra
		alt = np.array([_skysub.altit(dec[i],ha[i],sitelat)[0] for i in range(len(ha))])
		stg = alt.argmax()

		mm = obsmask[obsmask]
		mm[stg] = False
		obsmask[obsmask] = mm


		targets[tbin] = xaxis[stg]

		tbin+=1
	#print i
	return targets

####################################################################################################################################

def airmass(ra,dec,time,sitelat,sitelong):

	lst = _skysub.lst(time,sitelong) #*360./24.
	ha = lst - ra
	alt = _skysub.altit(dec,ha,sitelat)[0]

	return alt 