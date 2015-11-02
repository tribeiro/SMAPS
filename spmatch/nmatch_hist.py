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
    parser.add_option('-o','--output',
                    help = 'Output file.'
                    ,type='string')

    opt,args = parser.parse_args(argv)

    list = Table.read(opt.filename,format='hdf5',path='list')
    ulist = Table.read(opt.filename,format='hdf5',path='unknows')

    nmatch = np.zeros(len(list),dtype=[ ('n','<i4') ,
                                        ('SN_blue','<f8'),
                                        ('SN_mid' ,'<f8'),
                                        ('SN_red' ,'<f8')])

    listlen = len(list)
    print 'Working on %i entries... This may take some time...'%listlen

    for i,ff in enumerate(list['filename'][:listlen]):
        sys.stdout.write('\r-> %s (%7.3f %%) ...'%(ff,100.*i/listlen))
        sys.stdout.flush()
        try:
            m = Table.read(opt.filename,format='hdf5',path=ff)

            #a = store()
            #a.n = len(m)
            #a.spindex = np.unique(m['SPindex'])
            #a.spindex = [len(np.where(m['SPindex']==index)[0]) for index in np.unique(m['SPindex'])]
            #nmatch['n'][i] = a.n
            #nmatch['store'][i] = a

            nmatch['n'][i] = len(m)
            nmatch['SN_blue'][i] = ulist['SN_blue'][m['specindex'][0]]
            nmatch['SN_mid' ][i] = ulist['SN_mid' ][m['specindex'][0]]
            nmatch['SN_red' ][i] = ulist['SN_red' ][m['specindex'][0]]

        except KeyboardInterrupt:
            print ''
            print 'Exiting...'
            sys.exit(0)
        except:
            sys.stdout.write('[exc:%7i]'%i)
            sys.stdout.flush()
            pass

    print ' [Done]'
    if opt.output:
        np.save(opt.output,nmatch)
    #py.hist(nmatch,bins=np.arange(10.5,np.max(nmatch)+1.5))
    #py.show()

    return 0

################################################################################

if __name__ == '__main__':

    main(sys.argv)

################################################################################