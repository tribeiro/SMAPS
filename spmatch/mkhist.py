
import sys,os
import numpy as np
import pylab as py
from astropy.table import Table
from astropy.io import fits as pyfits
import re

def main(argv):

    _path = '/Volumes/TIAGOSD2/Documents/x.py/noWDs'
    filename = "match.npy"

    data = np.load(os.path.join(_path,filename))

    # m x logg x delta T
    mgrid = np.unique(data['mm_mod'])
    ggrid = np.unique(data['logg_mod'])
    mgrid.sort()
    ggrid.sort()
    X2,Y2 = np.meshgrid(mgrid,ggrid)
    print mgrid
    map = np.zeros((len(ggrid),len(mgrid)))

    mgrid = mgrid-0.5
    ggrid = ggrid-0.5
    mgrid = np.append(mgrid,mgrid[-1]+1.)
    ggrid = np.append(ggrid,ggrid[-1]+1.)

    diff = data['T_mod']-data['T_best']

    for ig in range(len(ggrid)-1):
        gmask = np.bitwise_and(data['logg_mod'] > ggrid[ig],
                               data['logg_mod'] < ggrid[ig+1])
        for im in range(len(mgrid)-1):
            # print ggrid[ig],ggrid[ig+1],mgrid[im],mgrid[im+1],map[ig][im]
            mmask = np.bitwise_and(data['mm_mod'] > mgrid[im],
                               data['mm_mod'] < mgrid[im+1])

            map[ig][im] = np.std(diff[np.bitwise_and(mmask,gmask)])

    #py.imshow(map,origin='lower',)
    # gmask = np.bitwise_and(data['logg_mod'] > -0.5,
    #                            data['logg_mod'] < 0.5)
    # mmask = np.bitwise_and(data['mm_mod'] > -0.5,
    #                data['mm_mod'] < 0.5)

    # py.hist(diff[np.bitwise_and(mmask,gmask)])
    # py.show()

    X,Y = np.meshgrid(mgrid,ggrid)
    # print X.shape,newhist.shape

    print X.shape
    print Y.shape
    print map.shape

    py.pcolor(X,Y,map,edgecolors='k')
    py.plot(X2,Y2,'k.')
    cbar = py.colorbar()

    py.xlabel('Metallicity')
    py.ylabel('Log g')
    cbar.set_label('$\\sigma \\Delta T$')
    py.show()

    return 0

if __name__ == "__main__":

    main(sys.argv)