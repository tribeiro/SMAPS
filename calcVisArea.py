#!/usr/bin/env python

import  sys,os
import healpy as H
import pylab as py 
from optparse import OptionParser
import numpy as np
import _skysub

def main(argv):
    '''
    Main function: Takes input parameters, read observability map, 
    select best areas, and show and/or save areas at an output file. 
    Run program with -h for help. 
    '''    

    parser = OptionParser()

    parser.add_option("-i",'--input',
                      help="Input file with masked healpy observability map (output of selectArea.py).",type="string")
    parser.add_option("-m",'--mask',
                      help="Extra mask to be readed (field 0 of output from selectArea.py).",type="string")
    parser.add_option("-f",'--field',default=0,
                      help="Field to be readed from input file. May be 0, 1 or 2, see selectArea.py for info.",type="int")
    parser.add_option("--phi_min",
                      help="Inferior limit on phi as spacial cut (default = 0 graus).",type="float",default=0.)
    parser.add_option("--phi_max",
                      help="Superior limit on phi as spacial cut (default = 180 graus).",type="float",default=180.)
    parser.add_option("--theta_min",
                      help="Inferior limit on theta as spacial cut (default = 0 graus).",type="float",default=-180)
    parser.add_option("--theta_max",
                      help="Superior limit on theta as spacial cut (default = 360).",type="float",default=360.)
    parser.add_option("-o",'--output',
                      help="Output file. ",type="string")
    parser.add_option('--save_mapped',
                      help="Output file for the masked map. Will store a healpy fits file with 1.0 for the marked areas and 0.0 otherwise.",type="string")
    parser.add_option("-s", '--show',action="store_true", default=False,
                      help="Show map before quiting. If no output file is given, then consider show=True.")
    parser.add_option("-c",'--coordinates',
                      help="Coordinates to use on spacial cut. Can be either 'G' (Galactic) or 'E' (Ecliptic). Default is 'G'.",type="string",default='G')
    parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")
    
    opt,arg = parser.parse_args(argv)

    if opt.input:
        if opt.verbose:
            print '(M):\n(M): Reading input file {0} ...\n(M):'.format(opt.input)
        obsMap = H.read_map(opt.input,field=opt.field)
    else:
        print '(E):\n(E): Input map not given.\n(E):'
        return -1

    emask = np.zeros(len(obsMap)) == 0
    if opt.mask:
        emask = H.read_map(opt.mask) == 1.
        if opt.verbose:
            print '''(R):
(R): Reading extra mask from {0} (assuming field = 0)... 
(R):'''.format(opt.mask)
        

    nside = H.npix2nside(len(obsMap))

    phi,theta = H.pix2ang(nside,np.arange(len(obsMap)))

    if opt.coordinates == 'E':
        print '''(R):
(R): Using ecliptic coordinates (J2000.). Convertion is made 
(R): elementwise and may take some time.
(R):''',
        sys.stdout.flush()
#        rate = 0.
#        sys.stdout.write('\r(R): {0:8.1f} %'.format(rate*10))
#        sys.stdout.flush()
        phi *= -180./np.pi
        phi += 90.
        theta *= 180./np.pi

        for i in range(len(phi)):
#            if rate != np.floor(i * 10. / len(phi)):
#                rate = np.floor(i * 10. / len(phi))
#                sys.stdout.write('\r(R): {0:8.1f} %'.format(rate*10))
#                sys.stdout.flush()
            phi[i],theta[i] = _skysub.gal2radec(theta[i],phi[i],2000.)

        mask_phi = np.bitwise_and(phi > opt.phi_min , phi < opt.phi_max)
        mask_theta = np.bitwise_and(theta > opt.theta_min ,theta < opt.theta_max )
        print

    else:
        print '''(R):
(R): Using galactic coordinates.
(R):'''
        mask_phi = np.bitwise_and(phi > opt.phi_min * np.pi / 180. , phi < opt.phi_max * np.pi / 180. )
        mask_theta = np.bitwise_and(theta > opt.theta_min * np.pi / 180. ,theta < opt.theta_max * np.pi / 180. )

#    print 'phi_min = {0}\nphi_max = {1}\ntheta_min = {2}\ntheta_max = {3}\n'.format(phi.min(),phi.max(),theta.min(),theta.max())

#    mask = np.bitwise_and(np.bitwise_and(mask_phi,mask_theta),obsMap > 0.)
    mask = np.bitwise_and(np.bitwise_and(mask_phi,mask_theta),emask)

    print '''(R):
(R): Npix_select = {npixs}
(R): Npix_s/Npix_tot = {rnpix}
(R): selected Area = {sarea} square-degree
(R): pixel Area = {parea} square-degree
(R): Avg Observability = {avgobs}
(R):'''.format(npixs = len(obsMap[mask]),
               sarea = len(obsMap[mask])*H.nside2pixarea(nside) * (180. / np.pi)**2.,
               avgobs = np.mean(obsMap[mask]), 
               rnpix = len(obsMap[mask]) * 1.0 / len(obsMap),
               parea = H.nside2pixarea(nside) * (180. / np.pi)**2. )

    obsMap[np.bitwise_not(mask)] = 0.

    if opt.output:

        amask = np.bitwise_and(np.bitwise_and(mask,obsMap == 0.),emask)
        fp = open(opt.output,'a')
        fp.write('{avgtime} {avgarea} {avgobs}\n'.format(avgtime = (opt.phi_max+opt.phi_min) * 0.5,
                                                         avgarea = len(obsMap[amask])*H.nside2pixarea(nside) * (180. / np.pi)**2.,
                                                         avgobs  = np.sum(obsMap[mask]) ) )
        fp.close()

    if opt.save_mapped:
        
        
        H.write_map(opt.save_mapped,obsMap,fits_IDL=False)

    if opt.show:
        #
        #H.cartview(phi,sub=(2,1,1),coord=['G','E'])

        
        amask = np.bitwise_and(mask,emask)
        obsMap[np.bitwise_not(amask)] = 0.
        #obsMap[emask] = 1.
        H.mollview(obsMap,sub=(2,1,1))
        H.cartview(obsMap,coord=['G','E'],sub=(2,1,2))

        py.show()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        help(main)
    else:
        main(sys.argv)

