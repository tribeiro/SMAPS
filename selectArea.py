#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Given an observability map, select areas with best observability until total area matches that specified by user.

Created on Wed Aug  1 11:22:12 2012

@author: tiago
"""

import  sys,os
import healpy as H
import pylab as py 
from optparse import OptionParser
import numpy as np

def findArea(img,npix,niter=100):
    
    imin,imed,imax = img.min(),img.mean(),img.max()

    mm = img > imed
    
    #
    # First selection, upper or lower half of brightness map
    #
    if len( img[mm] ) == npix:
        return mm
    elif len( img[mm] ) < npix:
        fsup = imed
        finf = imin
        
    else:
        fsup = imax
        finf = imed
    
    #
    # Iteration
    #
    spos = '|'+' '*50+'|'+' '*49+'|'
    pos = int(100 * len(img[mm]) / len(img) )
    targ = int ( 100 * npix / len(img) )
    spos = spos[:pos] + '+' + spos[pos+1:]
    spos = spos[:targ] + '^' + spos[targ+1:]
    
    print '[{0:4d}]'.format(0) + spos
    
    for i in range(niter):
        
        imed = (fsup+finf) / 2.
        
        mm = img > imed
    
        if len( img[mm] ) == npix:
            return mm
        elif len( img[mm] ) < npix:
            fsup = imed

        else:
            finf = imed
    
        spos = '|'+' '*50+'|'+' '*49+'|'
        pos = int(100 * len(img[mm]) / len(img) )
        targ = int ( 100 * npix / len(img) )
        spos = spos[:pos] + '+' + spos[pos+1:]
        spos = spos[:targ] + '^' + spos[targ+1:]

        if pos == targ:
            spos = spos[:targ] + 'x' + spos[targ+1:]
        
    
        print '[{0:4d}]'.format(i) + spos
    
    print '(W):\n(W):Could not find appropriate cut...\n(W):'
    
    return mm

def main(argv):
    '''
    Main function: Takes input parameters, read observability map, 
    select best areas, and show and/or save areas at an output file. 
    Run program with -h for help. 
    '''    

    parser = OptionParser()

    parser.add_option("-i",'--input',
                      help="Input file with healpy observability map.",type="string")
    parser.add_option("-a",'--area',
                      help="The total area (in square degrees) to be added with best observability.",type="float")
    parser.add_option("-o",'--output',
                      help="Output file. Will store a healpy fits file with 1.0 for the marked areas and 0.0 otherwise.",type="string")
    parser.add_option("-s", '--show',action="store_true", default=False,
                      help="Show map before quiting. If no output file is given, then consider show=True.")
    parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")
    
    opt,arg = parser.parse_args(argv)

    if opt.input:
        if opt.verbose:
            print '(M):\n(M): Reading input file {0} ...\n(M):'.format(opt.input)
        obsMap = H.read_map(opt.input)
    else:
        print '(E):\n(E): Input map not given.\n(E):'
        return -1
    
    if not opt.area:
        print '(E):\n(E): Total area not given. Please specify area for calculation.\n(E):'
        return -1
    elif opt.verbose:
        print '(M):\n(M): Total area: {0} square-degree...\n(M):'.format(opt.area)

    nside = H.npix2nside(len(obsMap))
    pixArea = H.nside2pixarea(nside) * (180. / np.pi)**2.
    npixArea = int(np.floor(opt.area/pixArea))
    if npixArea >= len(obsMap):
        print '''(E):
(E): Number of pixels to select ({0}) iguals to or larger 
(E): than total number of pixels ({1}). Doens't make sense
(E): to continue. Select a smaller area!
(E):'''.format(npixArea, len(obsMap))
        return -1
            
    if opt.verbose:
        print '(M):\n(M): Pixel area = {0} square-degree \n(M):'.format(pixArea)
        print '(M):\n(M): Total pixels = {0} \n(M):'.format(npixArea)

    mask = findArea(obsMap,npixArea)
        
    if not opt.output:
        print '(W):\n(W): No output file given, will show result after calculation.\n(W):'
        opt.show = True
    else:
        H.write_map(opt.output,
                    (mask,
                     obsMap*mask,
                     np.array(mask,dtype=float)*np.mean(obsMap[mask]) ),fits_IDL=False)
    
    if opt.show:
        
        H.mollview(mask)
        
        py.show()
        

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        help(main)
    else:
        main(sys.argv)

