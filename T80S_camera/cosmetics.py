#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
import pyfits
import matplotlib.cm as cm


##########################################################################################################

def countBadColumns(img,thresh=100):

	imgT=np.array(img.T)
	badcols = np.array([])
	
	sizeC = len(imgT)
	for i in range(sizeC):
		nbadpix = np.count_nonzero(imgT[i])
		if nbadpix > thresh:
			badcols = np.append(badcols,[i])
	return badcols

##########################################################################################################

def countBadPixels(img,bcols=[]):

	imgT=np.array(img.T)
	# Masking bad columns
	for i in bcols:
		imgT[i] = np.zeros_like(imgT[i])
	
	return np.count_nonzero(imgT)

##########################################################################################################

def main(argv):

	_path = '/Volumes/TiagoHD2/data/Grade5results'
	_path = '/Volumes/TiagoHD2/data/JPAS/11333-19-01'
	
	ifile = 'CCD0_Mode0_1x1_5Ke-CTE.fits'
	
	ifile = '11333-19-01_combine.fits'
	
	masks = [	'cool_new.fits',
				'cool_new_noros.fits' ,
				'hot_new.fits']
	
	title = [	'Cool pixels with buffers',
				'Cool pixels without buffers',
				'Hot pixel mask']

	masks = [	'cool_new_noros.fits' ,
				'hot_new.fits']

	masks = [	'hot0001.fits' ,
				'hot0005.fits' ,
				'hot0009.fits' ,
				'hot0013.fits' ,
				'hot0002.fits' ,
				'hot0006.fits' ,
				'hot0010.fits' ,
				'hot0014.fits' ,
				'hot0003.fits' ,
				'hot0007.fits' ,
				'hot0011.fits' ,
				'hot0015.fits' ,
				'hot0004.fits' ,
				'hot0008.fits' ,
				'hot0012.fits' ,
				'hot0016.fits' ]

	title = [	'CCD  0',
'CCD  1',
'CCD  2',
'CCD  3',
'CCD  4',
'CCD  5',
'CCD  6',
'CCD  7',
'CCD  8',
'CCD  9',
'CCD 10',
'CCD 11',
'CCD 12',
'CCD 13',
'CCD 14',
'CCD 15']
				
	#window = [100,100]

	#data = pyfits.getdata(os.path.join(_path,ifile))

	for i in range(len(masks)):
	
		sys.stdout.write('# - [%i/%i] Working on image %s ...'%(i+1,len(masks),masks[i]))
		sys.stdout.flush()

		data = pyfits.getdata(os.path.join(_path,masks[i]))
		
		bcols = countBadColumns(data)
		print ''
		print '## - Number of bad columns: %i'%(len(bcols))
		print '## - Bad columns @: '
		for bc in bcols:
			sys.stdout.write(' %i |'%bc)
		print
		bpix = countBadPixels(data,bcols)
		print '## - Number of bad pixels: %i'%(bpix)
				
		badpixels = np.where(data > 0)
		
		H,xedges,yedges = np.histogram2d(badpixels[0],
										 badpixels[1],
										bins=10,
										range = [ [0,9264] , [0,2400] ])
		
		fig = py.figure(i+1)
		
		ax = fig.add_subplot(1,1,1)
		
		#ax.axis("off")
		
		#py.setp(ax.get_yticklabels(),visible=False)
		#py.setp(ax.get_xticklabels(),visible=False)

		ax.imshow(	np.log10(H),
					extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]],
					interpolation='nearest',
					aspect='auto',
					origin='lower')
		xlim = py.xlim()
		ylim = py.ylim()
		for j in range(len(bcols)):
			ax.plot([bcols[j],bcols[j]],[yedges[0], yedges[-1]],'r:')
		
		py.ylim(ylim)
		py.xlim(xlim)
		ax.set_title(title[i])

		print '# - [DONE]'
		#py.imshow(data,interpolation='nearest',cmap = cm.gray,vmin=488,vmax=3099)

	py.show()


##########################################################################################################

if __name__ == '__main__':

	main(sys.argv)

##########################################################################################################