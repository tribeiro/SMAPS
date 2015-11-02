#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
#import pyfits
from astropy.io import fits as pyfits
import matplotlib.cm as cm

'''
sizex =  9432
sizey = 10016

bufferx = [ [4616 , 200] ,
			[0	  , 100] ,
			[9400 , 100]]

buffery = [	[   0 , 100] ,
			[1179 , 100] ,
			[2431 , 100] ,
			[3682 , 101] ,
			[4935 , 100] ,
			[6187 , 100] ,
			[7439 , 100] ,
			[8691 , 100] ,
			[9935 , 100] ]
'''
sizex = 9264
sizey = 2400

Quadrants = {   'Q1' : [ [4632, 4632] , [1200, 1200] ] ,
                'Q2' : [ [4632, 4632] , [0000, 1200] ] ,
                'Q3' : [ [0000, 4632] , [1200, 1200] ] ,
                'Q4' : [ [0000, 4632] , [0000, 1200] ] ,}
## Q1
#bufferx = [ [4632, 4632] ]
#buffery = [ [1200, 1200] ]

## Q2
#bufferx = [ [4632, 4632] ]
#buffery = [ [0000, 1200] ]

## Q3
#bufferx = [ [0000, 4632] ]
#buffery = [ [1200, 1200] ]

## Q4
bufferx = [ [0000, 4632] ]
buffery = [ [0000, 1200] ]

##########################################################################################################

def make_buffer(sx,sy,bfx,bfy):

	img = np.zeros(sx*sy).reshape(sx,sy) == 1

	for i in range(len(bfx)):
		img[bfx[i][0]:bfx[i][0]+bfx[i][1]] = True

	imgT = img.T
	for i in range(len(bfy)):
		imgT[bfy[i][0]:bfy[i][0]+bfy[i][1]] = True

	img = imgT.T

	return img

##########################################################################################################

def main(argv):

	#_path = '/Volumes/TiagoHD2/data/Grade5results'
	_path = '/Volumes/TiagoHD2/data/JPAS/11333-19-01/'
	_img = '11333-19-01_combine.fits'
	_ofile = 'buffer.fits'

	img = make_buffer(sizex,sizey,bufferx,buffery)

	py.imshow(img,interpolation='nearest',cmap = cm.gray,origin='lower')

	py.show()


##########################################################################################################

if __name__ == '__main__':

	main(sys.argv)

##########################################################################################################