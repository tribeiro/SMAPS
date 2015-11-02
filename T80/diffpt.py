#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py

################################################################################
def main(argv):
	
	from optparse import OptionParser
	
	parser = OptionParser()
	
	parser.add_option('-f','--filename',
					  help = 'Input spectrum to fit.'
					  ,type='string')
	parser.add_option('--tol',
					  help = "Tolerance.",
					  type='float',default=2.7)
	parser.add_option('--seeing',
					  help = "Seeing.",
					  type='float',default=2.5)
	parser.add_option('-v','--verbose',
					  help = 'Run in verbose mode.',action='store_true',
					  default=False)
	opt,args = parser.parse_args(argv)

	data = np.loadtxt(opt.filename,unpack=True)

	theta = np.linspace(0,1,100)

	py.plot(data[1]-np.mean(data[1]),data[2]-np.mean(data[2]),'bo')

	print np.std(data[1])*0.75,np.std(data[2])*0.75

	py.plot(opt.tol*np.sin(theta*2.*np.pi),opt.tol*np.cos(theta*2.*np.pi),'r-')
	py.plot(opt.seeing*np.sin(theta*2.*np.pi),opt.seeing*np.cos(theta*2.*np.pi),'g-')

	py.show()

	return 0

################################################################################

if __name__ == '__main__':

	main(sys.argv)

################################################################################