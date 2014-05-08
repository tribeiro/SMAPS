#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:34:03 2012

@author: tiago
"""

import sys,os
import healpy as H
import pylab as py 
import numpy as np
from matplotlib import rc

rc('text',usetex=False)

def main(argv):
    
    #
    # Basic definitions
    #
    _path = '/home/tiago/Develop/SMAPs/'

    file_area = [ 'dcorr_smpas_obstime_15_area12.fits'
                  ,'dcorr_smpas_obstime_15_area18.fits'
                  ,'dcorr_smpas_obstime_15_area6.fits'
                  ,'dcorr_smpas_obstime_2_area12.fits'
                  ,'dcorr_smpas_obstime_2_area18.fits'
                  ,'dcorr_smpas_obstime_2_area6.fits']
    
    #
    # Reading data
    #

    map_area = np.array([H.read_map(os.path.join(_path,file_area[0])),])

    for i in range(1,len(file_area)):
        map_area = np.append(map_area,np.array([H.read_map(os.path.join(_path,file_area[i])),]),axis=0)

    
    #
    # Plotting graph
    #


    ##
    ## This is best area cut observability
    ##

    plmap = np.zeros(map_area.shape[1])

    #for i in range(3):
    #    plmap += map_area[i]
    #
    #H.mollview(plmap,fig=1,title='secz < 1.5',coord=['G','E'],sub=(1,2,4),cbar=False,notext=True,max=3.5)
    #
    #plmap = np.zeros(map_area.shape[1])

    for i in range(3,len(map_area)):
        plmap += map_area[i]

    H.mollview(plmap,fig=1,title='',coord='G',sub=(2,1,1),cbar=False,notext=True,max=3.5)

    H.cartview(plmap,fig=1,title='',coord=['G','E'],sub=(2,1,2),cbar=False,notext=True,max=3.5)


    #
    # Finishing
    #
    py.savefig(os.path.join(_path,'Figures/fig3_bestarea.png'))

    py.show()

if __name__ == '__main__':
    
    main(sys.argv)
