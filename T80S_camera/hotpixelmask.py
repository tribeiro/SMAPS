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
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
                    level=logging.INFO)
##########################################################################################################

def main(argv):

    parser = OptionParser()

    parser.add_option("-i",'--input',
                      help="Input bias or dark image.",type="string")
    parser.add_option('--make-read-out-section',action="store_true",default=False,
                      help="Build read-out-section. This regions will be excluded from the bad pixel mask",
                      dest="make_ros")
    parser.add_option('--quadrant',default='Q1',type='string',
                      help="Default mask for quadrants. Q1, Q2, Q3 or Q4")
    parser.add_option("-o",'--output',
                      help="Output file. ",type="string")
    parser.add_option("--threshould",help="Limit for dark pixel count.",type="float",default=515.)
    parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")

    opt,arg = parser.parse_args(argv)

    logging.info('Reading in %s ...'%opt.input)
    
    data = pyfits.getdata(opt.input)
    badpixelmask = np.zeros_like(data)
    buffermask = np.zeros_like(data)
    if opt.make_ros:
        logging.info('Reading in pre-defined mask, Quadrant %s ...'%(opt.quadrant))
        buffermask = make_buffer.make_buffer(make_buffer.sizex,
                                             make_buffer.sizey,
                                             [make_buffer.Quadrants[opt.quadrant][0]],
                                             [make_buffer.Quadrants[opt.quadrant][1]])

        badpixelmask[buffermask] = 1

    threshould = opt.threshould
    if opt.threshould < 0:
        logging.info('# - Finding threshould automatically ...')
        avg = np.mean(data[badpixelmask == 0])
        #std = np.std(data[badpixelmask == 0])
        threshould = avg*1.2
    logging.info('Threshould = %.2f'%(threshould))

    logging.info('Searching for bad pixels ...')
	
    mask = data > threshould

    badpixelmask[mask] = 1
    badpixelmask[buffermask] = 0
    
    logging.info('DONE')
    nbad = np.count_nonzero(badpixelmask)
    totpix = badpixelmask.shape[0]*badpixelmask.shape[1]
    logging.info('Found %i/%i (%.4f) bad pixels'%(nbad,
                                                totpix,
                                                float(nbad)/totpix))

    logging.info('# - Writing bad pixel mask to %s...'%opt.output)

    pyfits.writeto(opt.output,np.array(badpixelmask,dtype=np.uint8))

    logging.info('Work complete!')

    return 0

##########################################################################################################

if __name__ == '__main__':

	main(sys.argv)

##########################################################################################################