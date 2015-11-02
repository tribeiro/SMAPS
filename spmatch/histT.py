__author__ = 'tiago'

import sys,os
import numpy as np
import pylab as py
from astropy.table import Table
from astropy.io import fits as pyfits
import re

def main(argv):

    _path = '/Volumes/TIAGOSD2/Documents/x.py/withWDs/'

    histName = 'histograma.fits'
    sptypesName = 'sptypes.txt'

    spt = Table.read(os.path.join(_path,sptypesName),
                     format='ascii.no_header')

    dtypeT = [('T','S6'),
        ('start',np.int),
        ('end',np.int)]
    dtypeL = [('logg','S6'),
        ('start',np.int),
        ('end',np.int)]
    dtypeM = [('mm','S4'),
        ('start',np.int),
        ('end',np.int)]
    tgrid = np.zeros(0,dtype=dtypeT)
    lgrid = np.zeros(0,dtype=dtypeL)
    mgrid = np.zeros(0,dtype=dtypeM)

    p = re.search('CK(?P<TEMP>\S+)-g(?P<LOGG>\S+)-(?P<MET>\S+)',
                   spt['col1'][0])
    t = p.group('TEMP')
    start = 0
    end = 0
    lastline = spt[0]

    ltmp = np.zeros(len(spt),dtype='S6')
    mtmp = np.zeros(len(spt),dtype='S4')
    ltmp[0] = p.group('LOGG')
    mtmp[0] = p.group('MET')

    for i,entry in enumerate(spt[1:]):
        p = re.search('CK(?P<TEMP>\S+)-g(?P<LOGG>\S+)-(?P<MET>\S+)',
                         entry[0])
        newt = p.group('TEMP')
        ltmp[i+1] = p.group('LOGG')
        mtmp[i+1] = p.group('MET')

        if newt != t:
            tgrid = np.append(tgrid,np.array((t,start,lastline[1]),dtype=dtypeT))
            start = entry[1]
            t = newt

        lastline = entry

    newhist = np.zeros((len(tgrid),len(tgrid)))

    hdata = pyfits.getdata(os.path.join(_path,histName))

    print 'Grid has %i temperatures'%len(tgrid)

    for i in range(len(tgrid)):
        for j in range(len(tgrid)):
            newhist[i][j] = np.mean(hdata[tgrid['start'][i]:tgrid['end'][i],
                                          tgrid['start'][j]:tgrid['end'][j]])

    lunique = np.unique(ltmp)
    munique = np.unique(mtmp)
    print 'Grid has %i logg'%len(lunique)
    print 'Grid has %i metalicities'%len(munique)

    # newhist[newhist == 0] = None
    #py.imshow(newhist,interpolation='nearest',origin='lower')

    X,Y = np.meshgrid(np.array(tgrid['T'],dtype=np.float),np.array(tgrid['T'],dtype=np.float))
    Z = np.vstack(newhist)
    # print X.shape,newhist.shape

    py.pcolor(X,Y,newhist)

    py.show()

    return 0

if __name__ == '__main__':
    main(sys.argv)