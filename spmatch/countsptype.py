#!/usr/bin/env python

__author__ = 'tiago'

import sys,os
import numpy as np
import pylab as py
from astropy.table import Table

################################################################################

def main(argv):

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option('-f','--filename',
                    help = 'Input hdf5 catalog.'
                    ,type='string')
    parser.add_option('--nmin',
                    help = 'Minimum number of matches.'
                    ,type='int')
    parser.add_option('--nmax',
                    help = 'Maximum number of matches. If not given consider nmatches == nmin.'
                    ,type='int')
    parser.add_option('-o','--output',
                    help = 'Output filename.'
                    ,type='string')
    opt,args = parser.parse_args(argv)

    if not opt.output:
        print 'Give output filename...'
        return -1

    list  = Table.read(opt.filename,format='hdf5',path='list')
    spt   = Table.read(opt.filename,format='hdf5',path='sptypes')
    ulist = Table.read(opt.filename,format='hdf5',path='unknows')

    histSPT = np.zeros((len(spt),len(spt)),dtype=int)

    listlen = len(list)
    print 'Working on %i entries... This may take some time...'%listlen

    Nmin = opt.nmin
    Nmax = opt.nmax
    if (not Nmax) or (Nmax < Nmin):
        Nmax = Nmin+1

    for i,ff in enumerate(list['filename'][:listlen]):
        sys.stdout.write('\r-> %s (%7.3f %%) ...'%(ff,100.*i/listlen))
        sys.stdout.flush()
        try:
            m = Table.read(opt.filename,format='hdf5',path=ff)
            if Nmin <= len(m) < Nmax:
                spindex = ulist['SPindex'][m['specindex'][0]]
                mtindex = m['SPindex'][1]
                histSPT[spindex][mtindex] += 1
        except KeyboardInterrupt:
            print ''
            print 'Exiting...'
            sys.exit(0)
        except:
            raise
            sys.stdout.write('[exc:%7i]'%i)
            sys.stdout.flush()
            pass

    print ' [Done]'
    print 'Saving result to %s ...'%opt.output
    np.save(opt.output,histSPT)

    return 0

################################################################################

if __name__ == '__main__':

    main(sys.argv)

################################################################################