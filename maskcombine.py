#!/usr/bin/env python

'''
	Combine mask images. Replace for imcombine, as I have no iraf installed yet.
'''

import sys,os
from optparse import OptionParser
import numpy as np
import pylab as py
#import pyfits
from astropy.io import fits as pyfits
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
                    level=logging.INFO)

################################################################################

def main(argv):
    
    parser = OptionParser()

    parser.add_option("-o",'--output',
        help="Output file. ",type="string")
    parser.add_option("-v", '--verbose',action="store_true", dest="verbose",
        default=False,
        help="Don't print status messages to stdout")

    opt,arg = parser.parse_args(argv)

    logging.info('%s'%(arg[1]))
    hdu = pyfits.open(arg[1])
    hdu[0].header['HISTORY'] = 'MASKCOMBINE:'
    hdu[0].header['HISTORY'] = '%s'%(arg[1])
    
    for fin in arg[2:]:
        logging.info('%s'%(fin))
        data = pyfits.getdata(fin)
        hdu[0].data += data
        hdu[0].header['HISTORY'] = '%s'%(fin)

    pyfits.writeto(opt.output,hdu[0].data,hdu[0].header)

    return 0

################################################################################

if __name__ == "__main__":

    main(sys.argv)

################################################################################