#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 15:18:56 2012

@author: tiago
"""

import  sys,os
import healpy as H
import pylab as py 
from optparse import OptionParser
import numpy as np
from matplotlib import colors
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection


def plotArea(area_x,area_y):
    for i in range(len(area_x)):
        if len(area_x[i]) > 1:
            x1 = np.linspace(area_x[i][0],area_x[i][1], 100) #np.arange(-100,110,10)
        else:
            x1 = np.zeros(100)+area_x[i]

        if len(area_y[i]) > 1:
            y1 = np.linspace(area_y[i][0],area_y[i][1], 100) #np.arange(-100,110,10)
        else:
            y1 = np.zeros(100)+area_y[i]

        H.projplot((90.-x1)*np.pi/180.,y1*np.pi/180.,'g',lw=2.)#,rot=(0,-90,90),coord=['G','E'])


def main(argv):

    _path = os.path.expanduser('~/Develop/SMAPs/')

    file_area = [  'dcorr_smpas_obstime_2_area12.fits'
                  ,'dcorr_smpas_obstime_2_area18.fits'
                  ,'dcorr_smpas_obstime_2_area6.fits']
    
    nna_file = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/norpointT80.dat')
    nsa_file = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/surpointT80.dat')
	
    smaps_sul = os.path.expanduser('~/Develop/SMAPs/smaps_pointsulT80.dat')
    smaps_nor = os.path.expanduser('~/Develop/SMAPs/smaps_pointT80norte.dat')


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

    for i in range(len(map_area)):
        plmap += map_area[i]
    
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['grey', 'blue', 'green', 'red'])

    H.mollview(plmap,coord=['G','E'],cmap=cmap,cbar=False,notext=True,title='S-MAPS Survey Area Selection')#,rot=(0,-90,90))#, norm=norm)
    #H.cartview(plmap,coord='G',cmap=cmap,cbar=False,notext=True,title='S-MAPS Survey Area Selection')#, norm=norm)
    H.graticule()

    nna_pt = np.loadtxt(nna_file,unpack=True,usecols=(4,5))
    nsa_pt = np.loadtxt(nsa_file,unpack=True,usecols=(4,5))

    pt_smaps_sul = np.loadtxt(smaps_sul,unpack=True,usecols=(4,5))
    pt_smaps_nor = np.loadtxt(smaps_nor,unpack=True,usecols=(4,5))

	
    #myPatches=[]

    #for i in range(len(nna_pt[0])):
    #    r2 = patches.RegularPolygon(((90-nna_pt[1][i])*np.pi/180.,nna_pt[0][i]*np.pi/180.),4,0.573*np.pi,orientation=45*np.pi/180.)
    #    myPatches.append(r2)
	

	#collection = PatchCollection(myPatches,alpha=0.5)
	#H.add_collection(collection)

    H.projplot((90-nna_pt[1])*np.pi/180.,nna_pt[0]*np.pi/180.,'.',color='w',alpha=0.5)#,coord=['E','G'])
    H.projplot((90-nsa_pt[1])*np.pi/180.,nsa_pt[0]*np.pi/180.,'.',color='w',alpha=0.5)#,coord=['E','G'])

    H.projplot((90-pt_smaps_sul[1])*np.pi/180.,pt_smaps_sul[0]*np.pi/180.,'.',color='k',alpha=0.5)#,coord=['E','G'])
    H.projplot((90-pt_smaps_nor[1])*np.pi/180.,pt_smaps_nor[0]*np.pi/180.,'.',color='k',alpha=0.5)#,coord=['E','G'])

    #
    # Area 1 - SGH
    #
    #sgh_x = [ [135,180] , [135, 120] , [ 120 , 105] , [ 105 ,  80] , [80 , 105] , [105]       , [105 , 180] ]
    #sgh_y = [ [100]     , [100 , 40] , [ 40 ]       , [ 40  , -55] , [-55, -60] , [-60 , -85] , [-85 ]
	    
    sgh_x = [ [135,180] , [135, 120] , [ 120 , 113.] , [ 113. ,  100] , [100 , 112] , [112]       , [112 , 180] ]
    sgh_y = [ [85]     , [85 , 25] , [ 25 ]       , [ 25  , -40] , [ -40] , [-40 , -65] , [-65 ]      ]
    
    #plotArea(sgh_x,sgh_y)
    
    #ngh_x1 = [ [135, 125] , [125,100] , [55,100]]
    #ngh_y1 = [ [180,130] , [130, 110] , [179,110]]

    ngh_x1 = [ [115] , [115,80] , [80]]
    ngh_y1 = [ [180,160] , [160] , [179.9,160]]

    #plotArea(ngh_x1,ngh_y1)

	#ngh_x2 = [ [135, 115]  , [115,55] , [55]]
    #ngh_y2 = [ [-180,-130] , [-130, -115] , [-115,-180]]

    ngh_x2 = [ [115] , [90,115] , [90]  , [90,65] , [65]]
    ngh_y2 = [ [-165,-180] , [-165] , [-165,-150] , [-150] , [-150,-180]]

	#plotArea(ngh_x2,ngh_y2)
	
    x1 = np.zeros(100)+np.pi/2. #np.linspace(0,np.pi/2.,100)
    y1 = np.linspace(-np.pi,np.pi,100)
    H.projplot(x1,y1,'w',lw=2.,coord=['G','E'])#,rot=(0,-90,90),coord=['G','E'])
    #H.projplot([0],[np.pi/2.],'ko',lw=2.,coord=['G','E'])#,rot=(0,-90,90),coord=['G','E'])
    H.projplot([192.859508],[27.128336],'ko',lw=2.,coord=['E'],lonlat=True)#,rot=(0,-90,90),coord=['G','E'])
    H.projplot([192.859508-180],[-27.128336],'wo',lw=2.,coord=['E'],lonlat=True)#,rot=(0,-90,90),coord=['G','E'])
    #H.projplot([-np.pi],[np.pi/2.],'wo',lw=2.,coord=['G','E'])#,rot=(0,-90,90),coord=['G','E'])
    #H.projplot([-np.pi],[0],'wo',lw=2.,coord=['G','E'])#,rot=(0,-90,90),coord=['G','E'])
#    ngh_x2 = [ [135, 115]  , [90, 115], [90,55] , [55]]
#    ngh_y2 = [ [-180,-120] , [-140, -120 ], [-140, -115] , [-115,-180]]
	
#    plotArea(ngh_x2,ngh_y2)
    py.savefig(os.path.join(_path,'Figures/areaSelection.pdf'))

    py.show()
    
if __name__ == '__main__':
    
    main(sys.argv)
