#! /usr/bin/env python

import sys,os
import numpy as np

def main(argv):

	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option('-f',"--filename",
                      help="Input filename.",type="string")

	parser.add_option('-c',"--catalog",
                      help="Input filename for catalog.",type="string")
    
	opt,arg = parser.parse_args(argv)

	f1 = np.loadtxt(opt.filename,dtype='S')
	f2 = np.loadtxt(opt.catalog,unpack=True,dtype='S')

	for f in f1:
		

if __name__ == '__main__':

	main(sys.argv)
