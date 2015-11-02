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

	parser.add_option('-f','--filename',
					  help = 'Input file name.'
					  ,type='string')

	parser.add_option('-v','--verbose',
					help = 'Run in verbose mode.',action='store_true',
					default=False)
	opt,args = parser.parse_args(argv)

	# read first as reference table
	tabxy = Table.read(opt.filename,format='ascii.no_header')
	
	hour = (tabxy['col1']-tabxy['col1'][0])*24.
	tabxy['col2'] -= tabxy['col2'][0]
	tabxy['col3'] -= tabxy['col3'][0]
	
	print 'stddev[x]     = ',np.std(tabxy['col2'])
	print 'stddev[y]     = ',np.std(tabxy['col3'])
	print 'stddev[total] = ',np.std(np.sqrt(tabxy['col2']**2. + tabxy['col3']**2.))
	
	ax1 = py.subplot(311)
	
	py.plot(hour,tabxy['col2'],'o')

	ylim = py.ylim()
	xlim = py.xlim()
	py.plot(xlim,[10.,10.],'k:')
	h = 3500./60./60,
	py.plot([h,h],ylim,'k:')
	py.ylim(ylim)
	
	
	ax2 = py.subplot(312)
	
	py.plot(hour,tabxy['col3'],'o')
	ylim = py.ylim()
	xlim = py.xlim()
	py.plot(xlim,[10.,10.],'k:')

	h = 3500./60./60,
	py.plot([h,h],ylim,'k:')
	py.ylim(ylim)

	ax3 = py.subplot(313)
	
	py.plot(hour,np.sqrt(tabxy['col2']**2. + tabxy['col3']**2.),'o')
	ylim = py.ylim()
	xlim = py.xlim()
	py.plot(xlim,[10.,10.],'k:')

	h = 3500./60./60,
	py.plot([h,h],ylim,'k:')
	py.ylim(ylim)

	ax1.set_ylabel('Drift in X [arcsec]')
	ax2.set_ylabel('Drift in Y [arcsec]')
	ax3.set_ylabel('Total drift [arcsec]')
	
	ax3.set_xlabel('Hours from start')
	
	py.setp(ax1.get_xticklabels(),visible=False)
	py.setp(ax2.get_xticklabels(),visible=False)
	py.subplots_adjust(hspace=0.1)
	
	py.show()

################################################################################

if __name__ == '__main__':

	main(sys.argv)

################################################################################