#!/usr/bin/env python 

'''
tileMaker.py - This routine is designed to produce a list of coordinates (Ra,Dec)
		pointings for a given surveyed area and telescope FoV size. The area
		parameter and telescope FoV are controled by command line parameters
		(run with -h for help page).

		Version 0 - 2012/Set/06

		Tiago Ribeiro - SOAR Telescope
'''

import  sys,os
import healpy as H
import pylab as py 
from optparse import OptionParser
import numpy as np
import _skysub
from  astropysics.coords.coordsys import EquatorialCoordinatesBase,LatLongCoordinates
#from StringIO import StringIO

################################################################################
#
#

def loadareas(ifile,check):
    '''
    Given a file with area definition, return the area vertex as a list of
    the input coordinates objects and a list of areas start/end indexes.
    Each area is defined by three coordinate points used to draw a triangle 
    in the sky. The user can build more complex areas by sticking triangles
    together. The file must have any multiple of 3 points (theta,phi), one 
    pair per line. The angle definition is:

    0 < theta < 180
    0 < phi < 360

    where theta = 0/180 are the north and south poles and phi = 90/270 the 
    East/West.

    '''

    _coords = np.loadtxt(ifile)

    _areas = np.arange(0,len(_coords)+3,3)

    return _areas,np.array(_coords)

#
#
################################################################################

################################################################################
#
#

def getnside(area):
    '''
    For a given 'area' in square-degrees return the appropriate nside for the 
    healpy pixelization algorithm.
    '''

    # Total area in square degrees
    totArea = 360.*360./np.pi

    # Approximate number of pixels is totArea / FoV area
    aprox_npix = totArea / area 

    return int( 2**np.ceil(np.log2(np.sqrt( aprox_npix/12 ) ) ) )

#
#
################################################################################

################################################################################
#
#

def getCoords(vertex,nside,rmap=True):
    '''
    Given vertex cordinates and nside for healpy pixelization, return all
    pointings that fall inside the defined area. By default (rmap=True)
    will return a healpy map of the ponitings inside the defined area. The
    user can use this to check the area selection. If rmap=False, will 
    return a list of coordinates (Ra,Dec) instead.
    '''

    npix = H.nside2npix(nside)

    center = [np.mean(vertex[0]),np.mean(vertex[1])]

    radii = np.max(np.sqrt( (vertex[0] - center[0])**2. + (vertex[1] - center[1])**2.) )
    ifar = np.argmax(np.sqrt( (vertex[0] - center[0])**2. + (vertex[1] - center[1])**2.) )

    vis = np.zeros(H.nside2npix(nside)) # == 1
    theta_map = np.zeros(H.nside2npix(nside))
    phi_map = np.zeros(H.nside2npix(nside))

    #
    # Make fist run to map possible pixels in the area with rought estimative.
    # Will store theta and phi map in memory to accelerate the more accurate 
    # process furthermore
    #
    for i in range(npix):
        
        theta,phi = H.pix2ang(nside,i)

        if ( np.sqrt( ( theta/np.pi*180. - center[0] )**2. + ( phi/np.pi*180. - center[1])**2. ) < radii ):
            vis[i] = True
            theta_map[i] = theta
            phi_map[i] = phi

        if phi > np.pi:
            phi-= 2.*np.pi

        if ( np.sqrt( ( theta/np.pi*180. - center[0] )**2. + ( phi/np.pi*180. - center[1])**2. ) < radii ):
            vis[i] = True
            theta_map[i] = theta
            phi_map[i] = phi#+2.*np.pi

        if vis[i]:

            #
            # Pixel may be inside area. 
            # Step 1) Identify 3 closest points that define visible area
            #
            P = np.array([theta_map[i]/np.pi*180.,phi_map[i]/np.pi*180.])
            A = np.array([[0.,0.],
                          [0.,0.],
                          [0.,0.]])
#            vertex2 = np.array(vertex)
            for j in range(len(A)):
                
                #iclose = np.argmin(np.sqrt( (vertex2[0] - center[0])**2. + (vertex2[1] - center[1])**2.) )
                A[j][0] = vertex[0][j]
                A[j][1] = vertex[1][j]
#                vertex2[0][iclose] = vertex[0][ifar]
#                vertex2[1][iclose] = vertex[1][ifar]

            v = np.array([ A[2] - A[0],
                           A[1] - A[0],
                           P    - A[0]])

            v12 = np.dot(v[1],v[2])
            v00 = np.dot(v[0],v[0])
            v02 = np.dot(v[0],v[2])
            v01 = np.dot(v[0],v[1])
            v11 = np.dot(v[1],v[1])
            v10 = np.dot(v[1],v[0])

            h = (v12 * v00 - v02 * v01) / (v11 * v00 - v10 * v01)
            u = (v11 * v02 - v01 * v12) / (v11 * v00 - v10 * v01)
            
            #print v12,v00,v02,v01,v11,v10,h,u
            #print A,P,v[0],v[1],v[2]

            vis[i] = ( (h >= 0.) and (u >= 0.) and (h+u <= 1.0) )

    if rmap:
        return center,vis
    else:
        rtheta,rphi = theta_map[vis],phi_map[vis]
        

#
#
################################################################################

################################################################################
#
#

def main(argv):

    '''
    Parse command line arguments and run tile procedure. For help and details
    about input/output parameters run with '-h' argument. 
    '''

    parser = OptionParser()

    parser.add_option('-a',"--areas",
                      help='''Definition of observing areas. The user must \
provide a list of reference points (Ra,Dec) that defines the edges of the \
surveyed area. Each area may be separated by a blanck line, so the program \
knows how many different areas where defined. The program will try to identify \
if the area makes any sense before running, and will emmit a warning in case it \
identify anything wrong). The user must make sure the area is ok before running \
the code.''',
                      type = 'string')

    parser.add_option('-f',"--field-of-view",
                      help='''The field of view area of the telescope/camera \
in square degrees. The procedure will find the higher uniform distribution of \
areas which are smaller than the specified field of view. Should the area \
overlap be smaller then desired, the user can try to specify a smaller FoV.''',
                      type='float')

    parser.add_option('-o',"--output",
                      help='''Output filename. This is an ascii text file \
where the program will write the coordinates to be observed.''',
                      type='string')

    parser.add_option("--check-areas",action="store_true", default=False,
                      help='''Check areas before proceeding to tiling? If \
checking, will issue an error message and stop should identify any problem\
 with the area definition. Skip checking by default.''')


    opt,arg = parser.parse_args(argv)

    if (not opt.areas) or (not opt.field_of_view):
        raise IOError('Input parameter (-a, -f or -o) unspecified.')


    def_areas,vert_coords = loadareas(opt.areas,check=opt.check_areas)

    print '(R): Read {0} areas:'.format(len(def_areas)-1)
    for i in range(len(def_areas)-1):
        print '(R): Area {0} is defined by {1} vertices.'.format(i+1,def_areas[i+1]-def_areas[i])

    print '(R):'

    nside = getnside(opt.field_of_view)

    print '''(R): FoV = {0}
(R): Mapped nside = {1}
(R): Number of fields = {2}
(R): Pixel Area = {3:.3f} square-degree
(R): Pixel Area overlap = {4:.1f}%
(R): '''.format(opt.field_of_view,
                nside,
                H.nside2npix(nside),
                H.nside2pixarea(nside) * (180. / np.pi)**2.,
                100*(1. - (H.nside2pixarea(nside) * (180. / np.pi)**2.) / opt.field_of_view))

    vis = np.zeros(H.nside2npix(nside))

    for i in range(len(def_areas)-1):
        
        vertx = np.array(vert_coords[def_areas[i]:def_areas[i+1]]).T
        coords,vis_tmp = getCoords(vertx,nside) 
        vis += vis_tmp

    mask = vis > 0
    totArea = len(vis[mask])*H.nside2pixarea(nside)
    print '''(R): Total area = {0}
(R): Npix = {1}
(R):'''.format(totArea * (180. / np.pi)**2.,len(vis[mask]))
	
    vis[mask] = 2.

    H.mollview(vis)

    #H.projplot(vertx[0]*np.pi/180,vertx[1]*np.pi/180.,'ro')
    coords = vert_coords.T
    H.projplot(coords[0]*np.pi/180,coords[1]*np.pi/180.,'ro')


    py.show()


    return 0

#
#
################################################################################

if __name__ == '__main__':

    if len(sys.argv) == 1:
        help('tileMaker')
    else:
        main(sys.argv)
