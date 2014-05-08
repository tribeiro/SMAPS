#!/usr/bin/env python

import os
import numpy as np
import pylab as py

def main():

	_path = os.path.expanduser('~/Develop/SMAPs/SPLUS')

	files = ['surveysim_04.txt','surveysim_05.txt']

	sdata0 = np.loadtxt(os.path.join(_path,files[0]),unpack=True)
	sdata1 = np.loadtxt(os.path.join(_path,files[1]),unpack=True)
	
	ax1 = py.subplot(211)
	
	py.fill_between(sdata0[0]-sdata0[0][0],sdata0[1],0)
	py.fill_between(x=sdata0[0]-sdata0[0][0],y1=sdata0[2],y2=0,color='green')
	#py.fill_between(x=sdata0[0]-sdata0[0][0],y1=sdata0[2]+sdata0[3],y2=sdata0[2],color='red')
	py.plot(sdata0[0]-sdata0[0][0],sdata0[1],'b-')
	#py.plot(sdata0[0]-sdata0[0][0],sdata0[2])
	#py.plot(sdata0[0]-sdata0[0][0],sdata0[3])
	#py.plot(sdata0[0]-sdata0[0][0],sdata0[4])
	#py.plot(tt[0]-tt[0][0],tt[4])

	#py.title('SPLUS Simulation - SLOAN (g and r) + All')
	py.ylabel('Hours')
	py.ylim(0.001,12)
	#py.xlabel('Day from 01/01/2014')

	ax2 = py.subplot(212)
	
	py.fill_between(sdata1[0]-sdata1[0][0],sdata1[2]+sdata1[3]+sdata1[4],sdata1[2]+sdata1[3])
	py.fill_between(x=sdata1[0]-sdata1[0][0],y1=sdata1[2],y2=0,color='green')
	py.fill_between(x=sdata1[0]-sdata1[0][0],y1=sdata1[2]+sdata1[3],y2=sdata1[2],color='red')
	py.plot(sdata1[0]-sdata1[0][0],sdata1[1],'b-')

	'''
	py.fill_between(sdata1[0]-sdata1[0][0],sdata1[1],0)
	py.fill_between(x=sdata1[0]-sdata1[0][0],y1=sdata1[2],y2=0,color='green')
	py.plot(sdata1[0]-sdata1[0][0],sdata1[1],'b-')
	#py.plot(tt[0]-tt[0][0],tt[3])
	#py.plot(tt[0]-tt[0][0],tt[4])
'''
	#py.title('SPLUS Simulation - All + repeat SLOAN (g and r)')
	py.ylabel('Hours')
	py.xlabel('Day from 01/01/2014')
	
	py.setp(ax1.get_xticklabels(),visible=False)
	
	py.subplots_adjust(hspace=0)
	py.ylim(0.,12)
	
	py.savefig(os.path.join(_path,'surveysim_04.pdf'))
	
	py.show()

if __name__ == '__main__':

	main()