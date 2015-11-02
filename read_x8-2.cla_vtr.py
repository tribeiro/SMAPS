#! /usr/bin/env python

import sys,os
import numpy as np
from astropy.table import Table
import logging as log

################################################################################

def main(argv):

    log.basicConfig(format='%(levelname)s:%(asctime)s::%(message)s',
                    level=log.DEBUG)

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option('-f','--filename',
                      help = 'Output file.'
                      ,type='string')
    parser.add_option('-v','--verbose',
                    help = 'Run in verbose mode.',action='store_true',
                    default=False)
    opt,args = parser.parse_args(argv)


    # Read list of unknows stored in this file
    ulist = Table.read( opt.filename,
                        path='list')

    log.info('A total of %i spectra stored in %s...'%(len(ulist),opt.filename))

    for i in range(len(ulist)):
        spres = Table.read( opt.filename,
                            path=ulist[i])
        log.info('Spectra %s has %i matches...'%(ulist[i],len(spres)))

    log.info('Done')

    return 0

################################################################################

if __name__ == '__main__':

    main(sys.argv)

################################################################################