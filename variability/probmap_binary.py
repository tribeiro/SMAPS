#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
import matplotlib.cm as cm


###################################################################################################

def main(argv):

	_path = os.path.expanduser('~/Documents/JPAS/variables/rdata/variability3/')

	_file = 'binary_p%02i.npy'

	nfiles = 46

	data = np.load(os.path.join(_path,_file%0))

	par = np.array([])
	prob = np.array([])
	
	for i,d in enumerate(data):
		par = np.append(par,d['par'])
		prob = np.append(prob,np.mean(d['prop']))
		#py.plot(d['snr'],d['prop'],'ro-')
	
	#print par
	#py.show()
	#return 0

	par = par.reshape(-1,3).T
	print len(np.unique(par[1])),len(prob)
	prob = prob.reshape(len(np.unique(par[1])),-1).T
	
	for i in range(1,nfiles):
		_data = np.load(os.path.join(_path,_file%i))
		_par = np.array([])
		_prob = np.array([])
		for j,d in enumerate(_data):
			_par = np.append(_par,d['par'])
			_prob = np.append(_prob,np.mean(d['prop']))
		_prob = _prob.reshape(len(np.unique(par[1])),-1).T
		prob += _prob

	py.subplot(211)
	
	im = py.imshow(	prob*100./45.,
					extent=[par[1][0],par[1][-1],par[2][0],par[2][-1]],
					aspect='auto',
					interpolation='nearest',
					origin='lower')#,cmap = cm.gray_r)
	py.colorbar(im)
	
	py.title('Probability of identifying variability on eclipsing binaries')
	py.xlabel('Eclipse Duration [$1/P_{orb}$]')
	py.ylabel('Amplitude [$\\Delta$ mag]')

	py.subplot(212)
	for ii,i in enumerate([0,10,44]):
		_data = np.load(os.path.join(_path,_file%i))
		color = ['r','b','g']
		ls = ['-','--',':']
		for jj,j in enumerate([80]):
			py.plot(_data[j]['snr'],_data[j]['prop']*100.,ls = ls[ii],color=color[jj])
		
	py.xlabel('S/N')
	py.ylabel('Detection prob.(%)')
	py.savefig(os.path.join(_path,'probmap_binary.pdf'))

	py.show()
	
	return 0

if __name__ == '__main__':

	main(sys.argv)