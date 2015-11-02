#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
from astropy.io import fits as pyfits

def main(argv):

	path = '/Volumes/TiagoSD/Documents/T80/Antonio_star'

	img = 'new-image.fits'

	hdu = pyfits.getheader(os.path.join(path,img))

	x = np.arange(0,hdu['IMAGEW'],40)-hdu['CRPIX1']
	y = np.arange(0,hdu['IMAGEH'],40)-hdu['CRPIX2']

	X,Y = np.meshgrid(x,y)

	NX = hdu['A_0_2']*Y**2.+hdu['A_1_1']*X*Y+hdu['A_2_0']*X**2.
	NY = hdu['B_0_2']*X**2.+hdu['B_1_1']*X*Y+hdu['B_2_0']*Y**2.
	
	'''
	py.figure(1)
	
	py.imshow(NX,origin='lower')

	py.figure(2)
	
	py.imshow(NY,origin='lower')
	'''
	Q = py.quiver( X[::3, ::3], Y[::3, ::3], NX[::3, ::3], NY[::3, ::3],
			   pivot='mid', color='r', units='inches' )
	#qk = py.quiverkey(Q, 0.5, 0.03, 1, r'$1 \frac{m}{s}$', fontproperties={'weight': 'bold'})
	py.plot( X[::3, ::3], Y[::3, ::3], 'k.')
	#py.axis([-1, 7, -1, 7])
	#py.title("pivot='mid'; every third arrow; units='inches'")
	py.xlim(-1500,1500)
	py.ylim(-1500,1500)
	py.show()

if __name__ == '__main__':

	main(sys.argv)