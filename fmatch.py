#! /usr/bin/env python

import sys,os
import numpy as np
import logging

logging.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
                    level=logging.INFO)

def main(argv):

	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option('-f',"--filename",
                      help="Input filename.",type="string")

	parser.add_option('-c',"--catalog",
                      help="Input filename for catalog.",type="string")

	parser.add_option('-o',"--output",
                    help="Output file.",type="string")

	opt,arg = parser.parse_args(argv)

	logging.info('Reading input file: %s'%opt.filename)
	f1 = np.loadtxt(opt.filename,dtype='S')
	logging.info('Reading catalog file: %s'%opt.catalog)
	f2 = np.loadtxt(opt.catalog,unpack=True,dtype='S',delimiter=',')
	rmatch = np.arange(len(f2[0]))

#	mask = f2[0] == f1[1]
#	print f1[1],f2[0][mask],f2[1][mask]
    
#	return 0
	fp = open(opt.output,'w')
	logging.info('XMatching...')
	for i in range(len(f1)):
		mask = f2[0] == f1[i]
		f = f2[0][mask]
		clss = f2[1][mask]
		scls = f2[2][mask]
		if len(f) > 0:
			fp.write('%s,%s,%s\n'%(f[0],clss[0],scls[0]))

	fp.close()
	logging.info('Done')


if __name__ == '__main__':

	main(sys.argv)
