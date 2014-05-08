#! /usr/bin/env python

'''
'''

import numpy as np
import pylab as py
import sys,os
import datetime

from chimera.util.position import Position

from chimera.controllers.scheduler.model import (Session, Targets, Program, Point,
                                                 Expose, PointVerify, AutoFocus, Projects)

from chimera.core.systemconfig import SystemConfig
from chimera.core.site import (Site, datetimeFromJD)

import _skysub


def datestr2JD(val):

	site = Site()

	return site.JD(datetime.datetime.strptime(val,'%Y-%m-%dT%H:%M:%S'))

def main(argv):

	path = os.path.expanduser('~/Documents/data_old/OPD40cm/20130809/')
	airmasstables = ['G9348/timeairmass.dat', 'SA111773/timeairmass.dat', 'SA114750/timeairmass.dat']
	#airmasstables = ['SA114750/timeairmass.dat']
	targetRa = [21.8736111111111,19.6211111111111,22.6958333333333]
	targetDec = [2.38888888888889,0.183055555555556,1.21055555555556]
	
	sitelat =-25.3416666667
	sitelong = 3.21148148148
	#airmasstables = np.loadtxt(os.path.join(path,airmasstableslis),dtype='S',ndmin=1)
		
	T0 = 2456514.
	nightstart = 2456514.4
	nightend = 2456514.85

	timeStamp = np.linspace(nightstart,nightend,1e3)
	
	lstStamp = [_skysub.lst(time,sitelong) for time in timeStamp]

	ax = py.subplot(111)
	ylim = [0,0.5]
	
	color = ['b','r','g','y','c','m', 'k']
	
	for i in range(len(airmasstables)):
		data = np.loadtxt(os.path.join(path,airmasstables[i]),unpack=True,converters={0:datestr2JD})
		secz = np.array([_skysub.true_airmass(_skysub.secant_z(_skysub.altit(targetDec[i],lst - targetRa[i],sitelat)[0])) for lst in lstStamp])
		data[1] = np.array([_skysub.true_airmass(_skysub.secant_z(_skysub.altit(targetDec[i],_skysub.lst(time,sitelong) - targetRa[i],sitelat)[0])) for time in data[0]])

		mm = np.bitwise_and(data[1] > 0, data[1] < 3)
		py.plot(data[0][mm]-T0,np.log10(data[1][mm]),color[i]+'o')
		py.plot(data[0][mm]-T0,np.log10(data[1][mm]),color[i]+'o')
		mm = np.bitwise_and(secz > 0, secz < 3)

		py.plot(timeStamp[mm]-T0,np.log10(secz[mm]),color[i]+'-')


	py.plot([nightstart-T0,nightstart-T0],ylim,'k--',lw=1.1,alpha=1.0)
	py.plot([nightend-T0,nightend-T0],ylim,'k--',lw=1.1,alpha=1.0)
	py.ylim(ylim[1],ylim[0])
	
	a=ax.get_yticks().tolist()
	print a
	newyticks = ['%.2f'%(10**(val)) for val in a]
	print newyticks
	ax.set_yticklabels(newyticks)

	py.ylabel('airmass',size=18)
	py.xlabel('JD - %.0f'%T0,size=18)
	py.savefig(os.path.expanduser('~/Develop/SMAPs/Figures/plot_airmasses_obs.pdf'))
	py.show()
		
	return 0

if __name__ == '__main__':

	main(sys.argv)