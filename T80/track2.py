#! /usr/bin/env

'''
	Get a list of files generated by phot and plot x,y coordinates of all 
	sources.
'''

import sys,os
import numpy as np
import pylab as py
from astropy.table import Table
from astropy.io import fits as pyfits
import logging

################################################################################

def main(argv):

	logging.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
						level=logging.DEBUG)
	
	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option('-v','--verbose',
					help = 'Run in verbose mode.',action='store_true',
					default=False)
	opt,args = parser.parse_args(argv)

	# read first as reference table
	mag0 = Table.read(args[1],format='ascii.daophot')
	

	xpos = np.zeros((len(args)-1))
	ypos = np.zeros((len(args)-1))
	expos = np.zeros((len(args)-1))
	eypos = np.zeros((len(args)-1))
	
	logging.info('Processing %i files with %i sources ...'%(len(args)-1,nstar))
	
	for ifile,mfile in enumerate(args[1:]):
		
		logging.debug('Reading %s ...'%mfile)
		
		mag0 = Table.read(mfile,format='ascii.daophot')

		xp = mag0['XCENTER'][0]
		yp = mag0['YCENTER'][0]
		xpos[istar][ifile] = mag0['XCENTER'][0]
		ypos[istar][ifile] = mag0['YCENTER'][0]


		expos[istar][ifile] = mag0['XERR'][0]
		eypos[istar][ifile] = mag0['YERR'][0]

	logging.info('Plotting...')

	py.errorbar(xp,yp,eypos,expos,fmt='o')

	py.show()

################################################################################

if __name__ == '__main__':

	main(sys.argv)

################################################################################