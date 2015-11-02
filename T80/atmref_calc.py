#! /usr/bin/env python

__author__ = 'tiago'

import sys,os
from chimera.util.position import Position
from chimera.core.site import (Site, datetimeFromJD)

from astropy.table import Table

from chimera.core.cli import ChimeraCLI, action

from dateutil import tz
import datetime as dt

import numpy as np
import pylab as py

def fromStr(istr):
    ddmmaaaa,hhmmss = istr.split('T')
    aaaa,mm,dd = ddmmaaaa.split('-')
    hh,MM,ss = hhmmss.split(':')

    return {'year'  : int(aaaa),
            'month' : int(mm),
            'day'   : int(dd),
            'hour'  : int(hh),
            'minute': int(MM),
            'second': int(ss),
            'tzinfo': tz.tzutc()}

class Atmref_calc(ChimeraCLI):

    #__config__ = {"file": ""}

    def __init__ (self):
        ChimeraCLI.__init__(self, "atmref_calc",
                            "Calculate atmosferic refrection", 0.0, port=9010)

        self.addController(name="site",
                           cls="Site",
                           required=True,
                           help="Observing site",
                           helpGroup="OBSERVATORY")

        self.addParameters(dict(name="filename", long="file", short="f",
                                default="",
                                help="Filename with parameters for scheduling algorith.",
                                metavar="FILENAME"))

    #def __start__ (self):
    #    self.calc("/Users/tiago/Develop/SMAPS/T80/80_min")

    @action(help="Select targets from specified project to be observed. ")
    def calc (self, arg):

        site = self.site

        data = Table.read(arg.filename,format='ascii.no_header')

        raDec = [Position.fromRaDec(data['col5'][i].split('.')[0],data['col6'][i].split('.')[0]) for i in range(len(data))]

        lst = np.array([site.LST(dt.datetime(**fromStr(data['col2'][i]))) for i in range(len(data))])

        altAz = [site.raDecToAltAz(raDec[i],lst[i]) for i in range(len(data))]

        pos_atmref = [1.02/np.tan( ( float(altAz[i].alt) + 10.3/(float(altAz[i].alt)+5.11) )*np.pi/180. ) for i in range(len(data))]

        #for i in range(len(data)):
        #    print lst[i], float(altAz[i].alt), data['col3'][i], pos_atmref[i]

        #py.plot(lst,
        #        [altAz[i].alt for i in range(len(data))],'.')

        #py.plot([altAz[i].alt for i in range(len(data))],
        #        [(pos_atmref[i]-pos_atmref[0])*60. for i in range(len(data))],'x')

        #py.savefig('foo1.png')
        #return 0

        newAltAz = [Position.fromAltAz(altAz[i].alt+pos_atmref[i]/60.,altAz[i].az) for i in range(len(data))]
        newRaDec = [site.altAzToRaDec(newAltAz[i],lst[i]) for i in range(len(data))]

        for i in range(len(data)):
            print data['col2'][i],lst[i], \
                data['col3'][i].split('.')[0],data['col4'][i].split('.')[0], \
                data['col5'][i],data['col6'][i], \
                newRaDec[i].ra,newRaDec[i].dec

        print float(newRaDec[0].ra),float(newRaDec[0].dec)
        print float(raDec[0].ra),float(raDec[0].dec)

        py.subplot(211)
        py.plot(lst,
                [-(newRaDec[i].dec-newRaDec[0].dec)*60.*60. for i in range(len(data))],
                'o-')
        py.subplot(212)
        py.plot(lst,
                [-(newRaDec[i].ra-newRaDec[0].ra)*24.*60. for i in range(len(data))],
                'o-')
        py.savefig('foo2.png')


################################################################################
def main():
    cli = Atmref_calc()
    cli.run(sys.argv)
    cli.wait()

################################################################################

if __name__ == '__main__':

    main()

################################################################################