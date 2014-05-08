#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
import matplotlib.cm as cm


###################################################################################################

def main(argv):

	_path = os.path.expanduser('~/Documents/JPAS/variables/rdata/variability3/')

	_file = 'pulsating_p45.npy'

	#decay_grid = np.append(np.arange(0.04,1,0.1),np.arange(1,10,0.25))
	
	#amplitude_grid = np.arange(0.01,1.0,0.02)
	
	#snr_grid = np.append(np.arange(5,15,1),np.arange(15,220+6,6))

	data = np.load(os.path.join(_path,_file))

	par = np.array([])
	prob = np.array([])
	
	for i,d in enumerate(data):
		par = np.append(par,d['par'])
		prob = np.append(prob,np.mean(d['prop']))
		#py.plot(d['snr'],d['prop'],'ro-')

	#py.show()
	
	#return 0
	print len(np.unique(par[1])),len(prob)
	par = par.reshape(-1,2).T
	sizex = len(np.unique(par[0]))
	sizey = len(np.unique(par[1]))
	map = np.zeros(sizex*sizey).reshape(sizex,sizey)

	for i in range(sizex):
		for j in range(sizey):
			map[i][j] = prob[i*sizey + j]
		#py.plot(par[1][:sizey],map[i],'r-o')

	py.subplot(211)

	im = py.imshow(	map.T*100.,
					extent=[par[0][0],par[0][-1],par[1][0],par[1][-1]],
					aspect='auto',
					interpolation='nearest',
					origin='lower')#,cmap = cm.gray_r)
	py.colorbar(im)
	
	py.title('Probability of identifying variability on transient objects')
	py.xlabel('Pulsation period [days]')
	py.ylabel('Amplitude [$\\Delta$ mag]')


	py.subplot(212)
	color = ['r','b','g']
	#ls = ['-','--',':']
	for jj,j in enumerate([49,41+23*46,46*50-1]):
		print data[j]['par']
		py.plot(data[j]['snr'],data[j]['prop']*100.,color=color[jj])
	py.ylim(50,101)

	py.xlabel('S/N')
	py.ylabel('Detection prob.(%)')
		
	py.savefig(os.path.join(_path,'probmap_pulsating.pdf'))

	py.show()
	
	return 0

if __name__ == '__main__':

	main(sys.argv)