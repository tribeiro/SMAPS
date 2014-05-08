#!/usr/bin/env python

'''
	Find defecting pixels on CCDs test images.
'''

import sys,os
import numpy as np
import pylab as py
import pyfits
import matplotlib.cm as cm
import make_buffer
import scipy.ndimage
import time
##########################################################################################################

def main(argv):

	_path = '/Volumes/TiagoHD2/data/Grade5results'
	ifile = 'CCD0_Mode0_1x1_5Ke-CTE.fits'
	
	window = [100,100]

	data = pyfits.getdata(os.path.join(_path,ifile))
	mask = np.zeros_like(data)


	buffermask = make_buffer.make_buffer(make_buffer.sizex,
										 make_buffer.sizey,
										 make_buffer.bufferx,
										 make_buffer.buffery)
	
	data = np.ma.masked_array(data,buffermask)
	
	#for i in range(len(data))
	
	#py.plot(data[ix])
	#yy = np.zeros(len(data[ix]))

	print time.strftime('%D %H:%M:%S')
	#scipy.ndimage.filters.median_filter(data,size=100,output=mask)
	
	
	for ix in range(len(data)):
		sys.stdout.write('\rWorking on line %i/%i'%(ix,len(data)))
		sys.stdout.flush()
		for iy in range(len(data[ix])):
			mask[ix][iy] = np.mean(data[ix-window[0]:ix+window[0],iy-window[1]:iy+window[1]])
	print ''
	print time.strftime('%D %H:%M:%S')
	
	#py.plot(yy,'.')
	
	pyfits.writeto('windoed100x100.fits',np.array(mask,dtype=float))

	py.imshow(mask,interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)

	py.show()
	
	return 0
	
	py.subplot(221)
	
	py.imshow(data[0:100,0:100],interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)

	py.subplot(222)

	py.imshow(data[0:100,100:200],interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)
	
	py.subplot(223)
	
	py.imshow(data[100:200,0:100],interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)

	py.subplot(224)
	
	py.imshow(data[100:200,100:200],interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)

	py.show()


##########################################################################################################

if __name__ == '__main__':

	main(sys.argv)

##########################################################################################################