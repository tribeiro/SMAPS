#!/usr/bin/env python

'''
	Find defecting pixels on CCDs test images.
'''

import sys,os
from optparse import OptionParser
import numpy as np
import pylab as py
#import pyfits
from astropy.io import fits as pyfits
import matplotlib.cm as cm
import make_buffer
import scipy.ndimage
import time
##########################################################################################################

def main(argv):

	parser = OptionParser()

	parser.add_option("-i",'--input',
	help="Input file with image to be searched for badpixels.",type="string")
	parser.add_option("-b",'--boxcar',
	help="Input file with boxcar image to be used as reference.",type="string")
	parser.add_option('--make-read-out-section',action="store_true",default=False,
	help="Build read-out-section. This regions will be excluded from the bad pixel mask",
	dest="make_ros")
	parser.add_option("-o",'--output',
	help="Output file. ",type="string")
	parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
	help="Don't print status messages to stdout")

	opt,arg = parser.parse_args(argv)

	print '# - Reading in %s ...'%opt.input
	data = pyfits.getdata(opt.input)
	print '# - Reading in %s ...'%opt.boxcar
	refdata = pyfits.getdata(opt.boxcar)
	badpixelmask = np.zeros_like(data)

	sys.stdout.write('# - Searching for bad pixels ...')
	sys.stdout.flush()
	
	mask = np.bitwise_or(data > refdata * 1.2, data < refdata * 0.8)
	
	badpixelmask[mask] = 1
	
	if opt.make_ros:
		sys.stdout.write('(masking read-out-section) ...')
		buffermask = make_buffer.make_buffer(make_buffer.sizex,
											 make_buffer.sizey,
											 make_buffer.bufferx,
											 make_buffer.buffery)
	
		badpixelmask[buffermask] = 0

	print '[DONE]'
	nbad = np.count_nonzero(badpixelmask)
	totpix = badpixelmask.shape[0]*badpixelmask.shape[1]
	print '# - Found %i/%i (%.4f) bad pixels'%(nbad,
												totpix,
												float(nbad)/totpix)
	
	sys.stdout.write('# - Writing bad pixel mask to %s...'%opt.output)
	sys.stdout.flush()

	pyfits.writeto(opt.output,np.array(badpixelmask,dtype=np.uint8))
	
	print '[DONE]'
	
	return 0

##########################################################################################################

if __name__ == '__main__':

	main(sys.argv)

##########################################################################################################