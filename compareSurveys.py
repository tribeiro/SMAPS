#!/usr/bin/env python

import os
import numpy as np
import pylab as py
import healpy as H
from matplotlib import colors
import matplotlib.cm as cm


def plotArea(area_x, area_y):
    for i in range(len(area_x)):
        if len(area_x[i]) > 1:
            x1 = np.linspace(area_x[i][0], area_x[i][1], 100)  # np.arange(-100,110,10)
        else:
            x1 = np.zeros(100) + area_x[i]

        if len(area_y[i]) > 1:
            y1 = np.linspace(area_y[i][0], area_y[i][1], 100)  # np.arange(-100,110,10)
        else:
            y1 = np.zeros(100) + area_y[i]

        H.projplot((90. - x1) * np.pi / 180., y1 * np.pi / 180., 'g', lw=2.)  # ,rot=(0,-90,90),coord=['G','E'])


################################################################################

def main():
    _path = os.path.expanduser('~/Develop/SMAPs/')

    file_area = ['lambda_sfd_ebv.fits']

    nna_file = os.path.expanduser('~/Develop/SMAPS/coordinatesystemandtiling2/norpointT80.dat')
    nsa_file = os.path.expanduser('~/Develop/SMAPS/coordinatesystemandtiling2/surpointT80.dat')

    smaps_sul = os.path.expanduser('~/Develop/SMAPs/smaps_pointsulT80.dat')
    smaps_nor = os.path.expanduser('~/Develop/SMAPs/smaps_pointT80norte.dat')
    smaps_lmc = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/foo3')
    smaps_smc = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/foo')

    allnovae = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/allnovae.txt')
    spp = os.path.expanduser('~/Develop/SMAPs/splus_varregions.dat')
    kepler = os.path.expanduser('~/Develop/SMAPS/coordinatesystemandtiling2/KeplerFOV')
    #
    # Reading data
    #

    map_area = np.array([H.read_map(os.path.join(_path, file_area[0])), ])

    for i in range(1, len(file_area)):
        map_area = np.append(map_area, np.array([H.read_map(os.path.join(_path, file_area[i])), ]), axis=0)

    #
    # Plotting graph
    #


    ##
    ## This is best area cut observability
    ##

    plmap = np.zeros(map_area.shape[1])

    cmap = colors.ListedColormap(['gray', 'blue', 'white', 'red'])

    H.mollview(map_area[0], coord=['G', 'E'], cmap=cm.gray_r, max=1, cbar=False, notext=True,
               title='J-PAS/J-PLUS/S-PLUS Survey Area')
    # H.mollview(map_area[0],cmap=cm.gray_r,max=1,cbar=False,notext=True,title='S-MAPS Survey Area Selection')

    # LMC
    #81.2102 -75.2561
    #H.projplot([(90+80.75)*np.pi/180.],[-69.5*np.pi/180.],'ko')
    #H.projplot([(90+81.2102)*np.pi/180.],[-75.2561*np.pi/180.],'ko')

    # SMC
    #302.8084 -44.3277
    #H.projplot([(90+13.0)*np.pi/180.],[-72.5*np.pi/180.],'ko')
    #H.projplot([302.8*np.pi/180.],[44.3*np.pi/180.],'wo')#,coord=['G','E'])

    #
    # Vista
    #
    ## VVV Bulge
    #

    b = np.append(np.append(np.append(np.linspace(80. * np.pi / 180., 95. * np.pi / 180., 100),
                                      np.zeros(100.) + 80. * np.pi / 180.),
                            np.linspace(80. * np.pi / 180., 95. * np.pi / 180., 100)),
                  np.zeros(100) + 96. * np.pi / 180.)

    l = np.append(np.append(np.append(np.zeros(100.) + 10. * np.pi / 180.,
                                      np.linspace(-10. * np.pi / 180., 10. * np.pi / 180., 100)),
                            np.zeros(100) - 10. * np.pi / 180.),
                  np.linspace(-10. * np.pi / 180., 10. * np.pi / 180., 100))
    H.projplot(b,l,'w-',lw=2,coord=['G','E'])

    #
    ## VVV Disk
    #

    b = np.append(np.append(np.append(np.linspace(88. * np.pi / 180., 92. * np.pi / 180., 100),
                                      np.zeros(100.) + 88. * np.pi / 180.),
                            np.linspace(88. * np.pi / 180., 92. * np.pi / 180., 100)),
                  np.zeros(100) + 92. * np.pi / 180.)

    l = np.append(np.append(np.append(np.zeros(100.) - 10. * np.pi / 180.,
                                      np.linspace(-10. * np.pi / 180., -65. * np.pi / 180., 100)),
                            np.zeros(100) - 65. * np.pi / 180.),
                  np.linspace(-65. * np.pi / 180., -10. * np.pi / 180., 100))
    H.projplot(b,l,'w-',lw=2,coord=['G','E'])


    ##################################
    # VPHAS

    vb = np.append(np.append(np.append(np.linspace(80. * np.pi / 180., 100. * np.pi / 180., 100),
                                      np.zeros(100.) + 80. * np.pi / 180.),
                            np.linspace(80. * np.pi / 180., 100. * np.pi / 180., 100)),
                  np.zeros(100) + 100. * np.pi / 180.)

    vl = np.append(np.append(np.append(np.zeros(100.) + 10. * np.pi / 180.,
                                      np.linspace(-10. * np.pi / 180., 10. * np.pi / 180., 100)),
                            np.zeros(100) - 10. * np.pi / 180.),
                  np.linspace(-10. * np.pi / 180., 10. * np.pi / 180., 100))
    # H.projplot(vb,vl,'r-',lw=2,coord=['G','E'])

    #
    ## VPHAS Disk
    #

    vb = np.append(np.append(np.append(np.linspace(85. * np.pi / 180., 95. * np.pi / 180., 100),
                                      np.zeros(100.) + 85. * np.pi / 180.),
                            np.linspace(85. * np.pi / 180., 95. * np.pi / 180., 100)),
                  np.zeros(100) + 95. * np.pi / 180.)

    vl = np.append(np.append(np.append(np.zeros(100.) + 40. * np.pi / 180.,
                                      np.linspace(40. * np.pi / 180., -160. * np.pi / 180., 100)),
                            np.zeros(100) - 160. * np.pi / 180.),
                  np.linspace(-160. * np.pi / 180., 40. * np.pi / 180., 100))
    H.projplot(vb,vl,'m-',lw=2,coord=['G','E'])


    #GAMA09:  08h36 < RA < 09h24,      -2 < Dec < +3 deg.


    nna_pt = np.loadtxt(nna_file, unpack=True, usecols=(4, 5))
    nsa_pt = np.loadtxt(nsa_file, unpack=True, usecols=(4, 5))

    pt_smaps_sul = np.loadtxt(smaps_sul, unpack=True, usecols=(4, 5))
    pt_smaps_nor = np.loadtxt(smaps_nor, unpack=True, usecols=(4, 5))
    # pt_allnovae = np.loadtxt(allnovae, unpack=True)
    pt_spp = np.loadtxt(spp, unpack=True, usecols=(4, 5))

    pt_kepler = np.loadtxt(kepler,unpack=True)
    #pt_smaps_smc = np.loadtxt(smaps_smc,unpack=True)

    #myPatches=[]

    #for i in range(len(nna_pt[0])):
    #    r2 = patches.RegularPolygon(((90-nna_pt[1][i])*np.pi/180.,nna_pt[0][i]*np.pi/180.),4,0.573*np.pi,orientation=45*np.pi/180.)
    #    myPatches.append(r2)


    #collection = PatchCollection(myPatches,alpha=0.5)
    #H.add_collection(collection)


    #H.projplot((90-pt_allnovae[1])*np.pi/180.,pt_allnovae[0]*np.pi/180.,'o',color='r',alpha=1,coord='E')#,coord=['E','G'])

    ####################################################################################################################
    # START S-PLUS
    #
    # S-PLUS Southern part
    #
    for line in np.arange(10, 30, 0.25):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-60, 61, 100)) * np.pi / 180., '-',
                   color='r', lw=1, alpha=0.9)
    for line in np.arange(30, 45, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-60, 91, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)
    for line in np.arange(45, 80, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-90, 90, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)

    # H.projplot((90 - np.zeros(100) + 9) * np.pi / 180., (np.linspace(-60, 61, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(10, 30, 100)) * np.pi / 180., (np.zeros(100) + 61) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 30) * np.pi / 180., (np.linspace(60, 90, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(30, 80, 100)) * np.pi / 180., (np.zeros(100) + 90) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 80) * np.pi / 180., (np.linspace(-90, 90, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(45, 80, 100)) * np.pi / 180., (np.zeros(100) - 90) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 45) * np.pi / 180., (np.linspace(-90, -60, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(10, 45, 100)) * np.pi / 180., (np.zeros(100) -60) * np.pi / 180., '-', color='r',
    #            lw=2)
    #
    # S-PLUS Northern part
    #
    for line in np.arange(0, 25, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(150, 180, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-157.5, -180, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)
    for line in np.arange(-15, 0, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(157.5,180, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)
    for line in np.arange(-30, 0, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-142.5,-180, 100)) * np.pi / 180., '-',
                   color='r', lw=2, alpha=0.9)

    # H.projplot((90 - np.zeros(100) + 25) * np.pi / 180., (np.linspace(150, 180, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(25, 0, 100)) * np.pi / 180., (np.zeros(100) + 150) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 0) * np.pi / 180., (np.linspace(150., 157.5, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(0, -15, 100)) * np.pi / 180., (np.zeros(100) + 157.5) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) - 15) * np.pi / 180., (np.linspace(157.5, 180, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    #
    # H.projplot((90 - np.zeros(100) + 25) * np.pi / 180., (np.linspace(-157.5, -180, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(25, 0, 100)) * np.pi / 180., (np.zeros(100) - 157.5) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 0) * np.pi / 180., (-1.*np.linspace(157.5, 142.5, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(0, -30, 100)) * np.pi / 180., (np.zeros(100) - 142.5) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) - 30) * np.pi / 180., (-1*np.linspace(142.5, 180, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # END S-PLUS
    ####################################################################################################################
    a = [0,0,5,5]
    d = [-3,+3,+3,-3]
    for d in np.arange(-3,3,0.5):
        H.projplot((90 - np.zeros(100) + d) * np.pi / 180., (np.linspace(0, 5, 100)) * np.pi / 180., '-', color='c',
               lw=2)

    # H.projplot((90 + np.linspace(10, 30, 100)) * np.pi / 180., (np.zeros(100) + 61) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 30) * np.pi / 180., (np.linspace(60, 90, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(30, 80, 100)) * np.pi / 180., (np.zeros(100) + 90) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 80) * np.pi / 180., (np.linspace(-90, 90, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(45, 80, 100)) * np.pi / 180., (np.zeros(100) - 90) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 45) * np.pi / 180., (np.linspace(-90, -60, 100)) * np.pi / 180., '-', color='r',
    #            lw=2)
    # H.projplot((90 + np.linspace(10, 45, 100)) * np.pi / 180., (np.zeros(100) -60) * np.pi / 180., '-', color='r',
    #            lw=2)


    H.projplot((90 - nna_pt[1]) * np.pi / 180., nna_pt[0] * np.pi / 180., '.', color='r', alpha=0.2,
               coord='E')  #,coord=['E','G'])
    H.projplot((90 - nsa_pt[1]) * np.pi / 180., nsa_pt[0] * np.pi / 180., '.', color='r', alpha=0.2,
               coord='E')  #,coord=['E','G'])

    H.projplot( (90-pt_kepler[1]) * np.pi/180. , pt_kepler[0] * np.pi /180., '-', color='c', alpha=1.0,
               coord='E',lw=2)  #,coord=['E','G'])


    # H.projplot((90 - pt_smaps_sul[1]) * np.pi / 180., pt_smaps_sul[0] * np.pi / 180., '.', color='r', alpha=0.2,
    #            coord='E')  #,coord=['E','G'])
    # H.projplot((90 - pt_smaps_nor[1]) * np.pi / 180., pt_smaps_nor[0] * np.pi / 180., '.', color='r', alpha=0.8,
    #            coord='E')  #,coord=['E','G'])

    # H.projplot((90 - pt_spp[1]) * np.pi / 180., pt_spp[0] * np.pi / 180., 'o',
    #            color='b', coord='E')  #,coord=['E','G'])

    #H.projplot((90-pt_smaps_lmc[1])*np.pi/180.,pt_smaps_lmc[0]*np.pi/180.,'.',color='k',alpha=1,coord='E')#,coord=['E','G'])
    #H.projplot((90-pt_smaps_smc[1])*np.pi/180.,pt_smaps_smc[0]*np.pi/180.,'.',color='k',alpha=1,coord='E')#,coord=['E','G'])

    H.graticule()

    # py.show()
    #
    # return 0
    # ATLAS

    for line in np.arange(10, 40, 1.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-37.5, 60, 100)) * np.pi / 180., ':',
                   color='g', lw=2, alpha=0.9)
    H.projplot((90 - np.zeros(100) + 42) * np.pi / 180., (np.linspace(-37.5, 61, 100)) * np.pi / 180., '-', color='g',
               lw=3)
    H.projplot((90 - np.zeros(100) + 10) * np.pi / 180., (np.linspace(-37.5, 61, 100)) * np.pi / 180., '-', color='g',
               lw=2)
    H.projplot((90 - np.linspace(-40, -10, 100)) * np.pi / 180., (np.zeros(100) + 62) * np.pi / 180., '-', color='g',
               lw=3)
    H.projplot((90 - np.linspace(-40, -10, 100)) * np.pi / 180., (np.zeros(100) - 37.5) * np.pi / 180., '-', color='g',
               lw=2)

    for line in np.arange(2, 29, 1.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(150, 180, 100)) * np.pi / 180., ':',
                   color='g', lw=2, alpha=0.9)
        if line < 20:
            H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-180, -127.5, 100)) * np.pi / 180., ':',
                       color='g', lw=2, alpha=0.9)
        else:
            H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-180, -135, 100)) * np.pi / 180., ':',
                       color='g', lw=2, alpha=0.9)

    H.projplot((90 - np.zeros(100) + 29) * np.pi / 180., (np.linspace(150, 180, 100)) * np.pi / 180., '-', color='g',
               lw=2)
    H.projplot((90 - np.zeros(100) + 20) * np.pi / 180., (np.linspace(-135, -127.5, 100)) * np.pi / 180., '-',
               color='g', lw=2)
    H.projplot((90 - np.zeros(100) + 29) * np.pi / 180., (np.linspace(-180, -135., 100)) * np.pi / 180., '-', color='g',
               lw=2)

    H.projplot((90 - np.zeros(100) + 2) * np.pi / 180., (np.linspace(150, 180, 100)) * np.pi / 180., '-', color='g',
               lw=2)
    H.projplot((90 - np.zeros(100) + 2) * np.pi / 180., (np.linspace(-180, -127.5, 100)) * np.pi / 180., '-', color='g',
               lw=2)

    H.projplot((90 - np.linspace(-29, -2, 100)) * np.pi / 180., (np.zeros(100) + 150) * np.pi / 180., '-', color='g',
               lw=2)
    H.projplot((90 - np.linspace(-20, -2, 100)) * np.pi / 180., (np.zeros(100) - 127.5) * np.pi / 180., '-', color='g',
               lw=2)
    H.projplot((90 - np.linspace(-29, -20, 100)) * np.pi / 180., (np.zeros(100) - 135) * np.pi / 180., '-', color='g',
               lw=2)

    # SPT

    H.projplot((90 - np.zeros(100) + 65) * np.pi / 180., (np.linspace(-60, 105, 100)) * np.pi / 180., '-', color='b',
               lw=2)

    # for line in np.arange(40, 65, 0.5):
    #     H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-60, 105, 100)) * np.pi / 180., '-',
    #                color='b', lw=2, alpha=0.5)
    H.projplot((90 - np.zeros(100) + 40) * np.pi / 180., (np.linspace(-60, 105, 100)) * np.pi / 180., '-', color='b',
               lw=2)
    # H.projplot((90 - np.zeros(100) + 40) * np.pi / 180., (np.linspace(-30, 105, 100)) * np.pi / 180., '--', color='b',
    #            lw=2)
    # H.projplot((90 - np.zeros(100) + 40) * np.pi / 180., (np.linspace(+60, 105, 100)) * np.pi / 180., '-', color='b',
    #            lw=2)

    H.projplot((90 - np.linspace(-65, -40, 100)) * np.pi / 180., (np.zeros(100) - 60) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.linspace(-65, -40, 100)) * np.pi / 180., (np.zeros(100) + 105) * np.pi / 180., '-', color='b',
               lw=2)

    # VIKING
    # for line in np.arange(25, 40, 0.5):
    #     H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-30, 60, 100)) * np.pi / 180., '-',
    #                color='b', lw=2, alpha=0.5)
    H.projplot((90 - np.linspace(-40, -25, 100)) * np.pi / 180., (np.zeros(100) - 30) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.linspace(-40, -25, 100)) * np.pi / 180., (np.zeros(100) + 60) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.zeros(100) + 25) * np.pi / 180., (np.linspace(-30, 60, 100)) * np.pi / 180., '-', color='b',
               lw=2)

    # ROUND 82
    # for line in np.arange(-3, 45, 0.5):
    #     H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-25, 3, 100)) * np.pi / 180., '-',
    #                color='b', lw=2, alpha=0.5)
    H.projplot((90 - np.linspace(3, -45, 100)) * np.pi / 180., (np.zeros(100) - 25) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.linspace(3, -45, 100)) * np.pi / 180., (np.zeros(100) + 3) * np.pi / 180., '-', color='b', lw=2)
    H.projplot((90 - np.zeros(100) + 45) * np.pi / 180., (np.linspace(-25, 3, 100)) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.zeros(100) - 3) * np.pi / 180., (np.linspace(-25, 3, 100)) * np.pi / 180., '-', color='b', lw=2)

    # STRIPE 82
    H.projplot((90 - np.linspace(-1, +1, 100)) * np.pi / 180., (np.zeros(100) - 3) * np.pi / 180., '-', color='b', lw=2)
    H.projplot((90 - np.linspace(-1, +1, 100)) * np.pi / 180., (np.zeros(100) - 43) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.zeros(100) + 1) * np.pi / 180., (np.linspace(-3, -43, 100)) * np.pi / 180., '-', color='b',
               lw=2)
    H.projplot((90 - np.zeros(100) - 1) * np.pi / 180., (np.linspace(-3, -43, 100)) * np.pi / 180., '-', color='b',
               lw=2)

    # KIDS

    H.projplot((90 - np.linspace(-5, +5, 100)) * np.pi / 180., (np.zeros(100) - 120) * np.pi / 180., '-', color='y',
               lw=2)
    H.projplot((90 - np.linspace(-5, +5, 100)) * np.pi / 180., (np.zeros(100) - 202.5) * np.pi / 180., '-', color='y',
               lw=2)

    for line in np.arange(-5, 5, 0.5):
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-120, -180, 100)) * np.pi / 180., '-',
                   color='y', lw=2, alpha=0.5)
        H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(157, 180, 100)) * np.pi / 180., '-',
                   color='y', lw=2, alpha=0.5)
    H.projplot((90 - np.zeros(100) - 5) * np.pi / 180., (np.linspace(157, 180, 100)) * np.pi / 180., '-', color='y',
               lw=2)
    H.projplot((90 - np.zeros(100) + 5) * np.pi / 180., (np.linspace(157, 180, 100)) * np.pi / 180., '-', color='y',
               lw=2)

    H.projplot((90 - np.zeros(100) - 5) * np.pi / 180., (np.linspace(-120, -180, 100)) * np.pi / 180., '-', color='y',
               lw=2)
    H.projplot((90 - np.zeros(100) + 5) * np.pi / 180., (np.linspace(-120, -180, 100)) * np.pi / 180., '-', color='y',
               lw=2)

    H.projplot((90 - np.linspace(-30, -25, 100)) * np.pi / 180., (np.zeros(100) - 30) * np.pi / 180., '-', color='y',
               lw=2)
    H.projplot((90 - np.linspace(-30, -25, 100)) * np.pi / 180., (np.zeros(100) + 30) * np.pi / 180., '-', color='y',
               lw=2)
    for line in np.arange(-30, -25, 0.5):
        H.projplot((90 - np.zeros(100) - line) * np.pi / 180., (np.linspace(-30, 30, 100)) * np.pi / 180., '-',
                   color='y', lw=2, alpha=0.5)

    H.projplot((90 - np.zeros(100) + 30) * np.pi / 180., (np.linspace(-30, 30, 100)) * np.pi / 180., '-', color='y',
               lw=2)
    H.projplot((90 - np.zeros(100) + 25) * np.pi / 180., (np.linspace(-30, 30, 100)) * np.pi / 180., '-', color='y',
               lw=2)

    #
    ## VIKING
    #

    #SGP:        22h00 < RA < 03h30 ,     -36 < Dec < -26 deg.
    H.projplot((90 - np.zeros(100) + 45.) * np.pi / 180., (np.linspace(-36, -26, 100)) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.linspace(-45, 30, 100)) * np.pi / 180., (np.zeros(100) - 36) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.zeros(100) - 30.) * np.pi / 180., (np.linspace(-36, -26, 100)) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.linspace(-45, 30, 100)) * np.pi / 180., (np.zeros(100) - 26) * np.pi / 180., '-', color='k',
               lw=2)
    # for line in np.arange(-45, 30, 0.5):
    #     H.projplot((90 - np.zeros(100) - line) * np.pi / 180., (np.linspace(-36, -26, 100)) * np.pi / 180., '-',
    #                color='k', lw=2, alpha=0.5)
    #NGP:        10h00 < RA < 15h30,      -5 < Dec < +4 deg
    H.projplot((90 - np.zeros(100) + 150.) * np.pi / 180., (np.linspace(-5, 4, 100)) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.linspace(-150, -232.5, 100)) * np.pi / 180., (np.zeros(100) + 4) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.zeros(100) + 232.5) * np.pi / 180., (np.linspace(-5, +4, 100)) * np.pi / 180., '-', color='k',
               lw=2)
    H.projplot((90 - np.linspace(-150, -232.5, 100)) * np.pi / 180., (np.zeros(100) - 5) * np.pi / 180., '-', color='k',
               lw=2)
    # for line in np.arange(150, 232.5, 0.5):
    #     H.projplot((90 - np.zeros(100) + line) * np.pi / 180., (np.linspace(-5, +4, 100)) * np.pi / 180., '-',
    #                color='k', lw=2, alpha=0.5)

    H.graticule()

    py.show()

################################################################################

if __name__ == '__main__':
    main()