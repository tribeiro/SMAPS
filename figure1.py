#!/usr/bin/env python

import sys,os
import healpy as H
import pylab as py 
import numpy as np

def main(argv):

    _path = os.path.expanduser('~/Develop/SMAPs/')
    nna_file = os.path.expanduser('~/Documents/SMAPs/norpointT80.dat')
    nsa_file = os.path.expanduser('~/Documents/SMAPs/surpointT80.dat')

    sna_file = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/smaps_pointT80norte.dat')
    ssa_file = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/smaps_pointsulT80.dat')

    nna_pt = np.loadtxt(nna_file,unpack=True,usecols=(4,5))
    nsa_pt = np.loadtxt(nsa_file,unpack=True,usecols=(4,5))

    sna_pt = np.loadtxt(sna_file,unpack=True,usecols=(4,5))
    ssa_pt = np.loadtxt(ssa_file,unpack=True,usecols=(4,5))
		
    file1 = 'lambda_sfd_ebv.fits' 
    file2 = 'smpas_obstime_2.fits'
    file3 = 'smpas_obstime_15.fits'
    extMapFile = 'extintion_at3800.fits'
    
    map1 = H.read_map(os.path.join(_path,file1))
    map2 = H.read_map(os.path.join(_path,file2))
    map3 = H.read_map(os.path.join(_path,file3))    
    extMap = H.read_map(os.path.join(_path,extMapFile))
    
    H.mollview(map1,fig=1,coord=['G','E'],max=1.0,title='',sub=(2,2,3),cbar=False,notext=True)#,unit='hours z < 1.3')

    H.projplot((90-nna_pt[1])*np.pi/180.,nna_pt[0]*np.pi/180.,'r.')#,coord=['E','G'])
    H.projplot((90-nsa_pt[1])*np.pi/180.,nsa_pt[0]*np.pi/180.,'r.')#,coord=['E','G'])

    H.projplot((90-sna_pt[1])*np.pi/180.,sna_pt[0]*np.pi/180.,'w.')#,coord=['E','G'])
    H.projplot((90-ssa_pt[1])*np.pi/180.,ssa_pt[0]*np.pi/180.,'w.')#,coord=['E','G'])

    H.graticule()

    H.mollview(map2,fig=1,coord=['G','E'],title='',sub=(2,2,1),cbar=False,notext=True,max=1800)
	#,unit='hours z < 1.3')

    H.graticule()

    H.mollview(map3,fig=1,coord='G',title='',sub=(2,2,2),cbar=False,notext=True,max=1800)#,unit='hours z < 1.3')

    H.graticule()

    H.mollview(map2*10**(-extMap),fig=1,coord='G',title='',sub=(2,2,4),cbar=False,notext=True)#,unit='hours z < 1.3')

    H.graticule()

    py.savefig(os.path.join(_path,'Figures/fig1.png'))

    py.show()

if __name__ == '__main__':

    main(sys.argv)
