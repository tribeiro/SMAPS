#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
import pyfits
import matplotlib.cm as cm

def main(argv):

	_path = os.path.expanduser('~/images/20131005/')
	_flist = 'point_test.lis'
	
	filenames = np.loadtxt(os.path.join(_path,_flist),dtype='S')
	fig = py.figure(1)
	ax = fig.add_subplot(1,1,1) #[fig.add_subplot(2,2,0),fig.add_subplot(2,2,1),fig.add_subplot(2,2,2),fig.add_subplot(2,2,3)]
	#ax = fig.add_axes([0,0,1,1])
	ax.axis("off")

	for fname in filenames:
		data = pyfits.getdata(os.path.join(_path,fname))
		ax.axis("off")
		ax.imshow(	data,
					vmin=data.min(),
					vmax=0.01*data.max()+data.min(),
					interpolation='nearest',
					cmap = cm.gray)
		py.title(fname)
		#py.show()
		py.savefig(os.path.join(_path,fname.replace('.fits','.png')))
		print os.path.join(_path,fname),' -> ',os.path.join(_path,fname.replace('.fits','.png'))
		py.cla()


if __name__ == '__main__':

	main(sys.argv)