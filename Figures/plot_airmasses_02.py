#! /usr/bin/env python

'''
'''

import numpy as np
import pylab as py
import sys,os

def main(argv):

	path = os.path.expanduser('~/Develop/SMAPs/Figures/data')
	airmasstableslis = 'airmasstable.lis'
	airmasstables = np.loadtxt(os.path.join(path,airmasstableslis),dtype='S',ndmin=1)
	
	T0 = 2456563
	nightstart = 2456563.436 - T0
	nightend = 2456563.820 - T0
	
	ax = py.subplot(111)
	ylim = [0,0.5]
	
	color = ['b']
	
	for i in range(len(airmasstables)):
		data = np.loadtxt(os.path.join(path,airmasstables[i]),unpack=True)
		mm = np.bitwise_and(data[1] > 0, data[1] < 3)
		#py.plot(data[0][mm]-T0,np.log10(data[1][mm]),'b')
		py.fill_between(x=data[0][mm]-T0,y1=np.log10(data[1][mm]),y2=ylim[1],color='b')
		
	py.plot([nightstart,nightstart],ylim,'k--',lw=1.1,alpha=1.0)
	py.plot([nightend,nightend],ylim,'k--',lw=1.1,alpha=1.0)
	py.ylim(ylim[1],ylim[0])
	
	a=ax.get_yticks().tolist()
	print a
	newyticks = ['%.2f'%(10**(val)) for val in a]
	print newyticks
	ax.set_yticklabels(newyticks)

	py.ylabel('airmass',size=18)
	py.xlabel('JD - 2456563',size=18)
	py.savefig(os.path.expanduser('~/Develop/SMAPs/Figures/plot_airmasses_02.pdf'))
	py.show()
		
	return 0

if __name__ == '__main__':

	main(sys.argv)