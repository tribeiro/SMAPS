#! /usr/bin/env python

'''
	Read tiles for smaps and select tiles inside a user specified ra,dec,radius region.
'''

import sys,os
import numpy as np
from astropy.coordinates import ICRS
from astropy import units as u


################################################################################

def main(argv):

	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option("-f",'--filename',
                      help='''File specifing the coordinates and size (ra dec radius)
for selecting tiles.
''',
					  type="string")
	parser.add_option("-o",'--output',
                      help="Name of file to be written the results.",
					  type="string")
	parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")
    
	opt,arg = parser.parse_args(argv)

	#
	# Read tiles
	#
	smaps_sul = os.path.expanduser('~/Develop/SMAPs/smaps_pointsulT80.dat')
	smaps_nor = os.path.expanduser('~/Develop/SMAPs/smaps_pointT80norte.dat')

	tiles_sul = np.loadtxt(smaps_sul,unpack=True)
	tiles_nor = np.loadtxt(smaps_nor,unpack=True)

	fp = open(smaps_sul,'r')
	suldata = fp.readlines()
	fp.close()

	fp = open(smaps_nor,'r')
	nordata = fp.readlines()
	fp.close()

	tiles_sul_icrs = np.array([ICRS(tiles_sul[4][i],tiles_sul[5][i],unit=(u.degree,u.degree)) for i in range(len(tiles_sul[0]))])

	tiles_nor_icrs = np.array([ICRS(tiles_nor[4][i],tiles_nor[5][i],unit=(u.degree,u.degree)) for i in range(len(tiles_nor[0]))])
	#
	# Read coordinates
	#
	coo = np.loadtxt(opt.filename,unpack=True,ndmin=2)
	
	coo_icrs = np.array([ICRS(coo[0][i],coo[1][i],unit=(u.degree,u.degree)) for i in range(len(coo[0]))])
	
	fp = open(opt.output,'w')
	
	for i in range(len(coo[0])):
		print '# Selecting tiles around %.2f,%.2f (r=%.2f)'%(coo[0][i],coo[1][i],coo[2][i])
		
		sys.stdout.write('## - Calculating separation, this may take some time. Slow but reliable...')
		sys.stdout.flush()
		sepsul = np.array([tiles_sul_icrs[j].separation(coo_icrs[i]).degree for j in range(len(tiles_sul_icrs))])
		sepnor = np.array([tiles_nor_icrs[j].separation(coo_icrs[i]).degree for j in range(len(tiles_nor_icrs))])

		print ' [DONE]'
		masksul = sepsul < coo[2][i]
		masknor = sepnor < coo[2][i]
		#tiles = np.append(tiles_sul_icrs[masksul],tiles_nor_icrs[masknor])
		sindex = np.arange(len(sepsul))[masksul]
		nindex = np.arange(len(sepnor))[masknor]
		for si in sindex:
			fp.write(suldata[si])
		for ni in nindex:
			fp.write(nordata[ni])
	fp.close()
		#for tile in tiles:
		#	print tile.ra.degree,tile.dec.degree
		#	#print tile.to_string(precision=3,sep=':')

	
	return 0

################################################################################

if __name__ == '__main__':

	main(sys.argv)