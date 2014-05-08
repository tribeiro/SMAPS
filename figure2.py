#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Wed Aug  1 10:46:49 2012

@author: tiago
'''

import  sys,os
import healpy as H
import pylab as py 
#import numpy as np
from matplotlib import rc

rc('text',usetex=False)

def main(argv):
    
    _path = '/home/tiago/Develop/SMAPs/'

    file15 = 'smpas_obstime_15.fits'
    file2 = 'smpas_obstime_2.fits'
    extMapFile = 'extintion_at3800.fits'
    
    map15 = H.read_map(os.path.join(_path,file15))
    map2 = H.read_map(os.path.join(_path,file2))    
    extMap = H.read_map(os.path.join(_path,extMapFile))

    fig = py.figure(1,figsize=(8,3))

    H.mollview(map2*10**(-extMap),fig=1,coord=['G','E'],title='secz < 2.0',sub=(1,2,1),max=1296,cbar=False,notext=True)#,unit='hours z < 1.3')

    H.graticule()

    H.mollview(map15*10**(-extMap),fig=1,coord=['G','E'],title='secz < 1.5',sub=(1,2,2),max=1296,cbar=False,notext=True)#,unit='hours z < 1.3')

    H.graticule()

    #H.write_map(os.path.join(_path,'dcorr_'+file15),map15*10**(-extMap))
    #H.write_map(os.path.join(_path,'dcorr_'+file2),map2*10**(-extMap))
    #H.write_map(os.path.join(_path,'dcorr_'+file3),map3*10**(-extMap))

    py.savefig(os.path.join(_path,'Figures/fig2.png'))

    py.show()
    
if __name__ == '__main__':
    
    main(sys.argv)