#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Wed Aug  1 10:46:49 2012

@author: tiago
'''

import  sys,os
import pylab as py 
import numpy as np

def main(argv):
    
	_path = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling')

	smaps_sul = 'smaps_pointsulT80.dat'
	smaps_nor = 'smaps_pointT80norte.dat'

	jpas_nor = 'norpointT80.dat'
	jpas_sul = 'surpointT80.dat'
	
	pt_smaps_sul = np.loadtxt(os.path.join(_path,smaps_sul),unpack=True)
	pt_smaps_nor = np.loadtxt(os.path.join(_path,smaps_nor),unpack=True)
	
	pt_jpas_sul = np.loadtxt(os.path.join(_path,jpas_sul),unpack=True)
	pt_jpas_nor = np.loadtxt(os.path.join(_path,jpas_nor),unpack=True)
	
	py.plot(pt_jpas_sul[4],pt_jpas_sul[5],'b.')
	py.plot(pt_jpas_nor[4],pt_jpas_nor[5],'b.')
	
	py.plot(pt_smaps_sul[4],pt_smaps_sul[5],'r.')
	py.plot(pt_smaps_nor[4],pt_smaps_nor[5],'r.')
	
	py.xlim(0,360)
	py.ylim(-90,90)
	py.grid()
	#py.savefig(os.path.join(_path,'tiles.png'))

	py.show()
    
if __name__ == '__main__':
    
    main(sys.argv)