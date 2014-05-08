#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 17:57:35 2012

@author: tiago
"""

import  sys,os
import pylab as py 
import numpy as np
#from matplotlib import rc

#rc('text',usetex=False)

def main(argv):
    
    _path = '/home/tiago/Develop/SMAPs/'

    mobsFile = 'montly_obs.dat'
    
    mobs = np.loadtxt(os.path.join(_path,mobsFile),unpack=True,usecols=(1,))
    
    ra = np.arange(0,26,2)

    fig = py.figure(1)
    
    ax1 = py.subplot(121)
    
    ax2 = py.subplot(122,sharey=ax1)
  
    ax1.plot(ra[6:],np.append(mobs[-1],mobs[:6]),ls='steps-mid',color='k')

#    ax1.plot(ra[7:],mobs[:6],ls='steps-mid')
    
    ax2.plot(ra[:7],mobs[5:],ls='steps-mid',color='k')
    
    py.setp(ax2.get_yticklabels(),visible=False)
    py.setp(ax2.get_xticklabels(),fontsize=20)
    py.setp(ax1.get_yticklabels(),fontsize=20)
    py.setp(ax1.get_xticklabels(),fontsize=20)
    
    print 'DONE'
    
    ax1.set_xlim(11.9,23.99)
    ax2.set_xlim(0,12.1)
    ax1.set_ylim(0,1700)
    ax1.set_ylabel('Area',fontsize=20)
    
    py.subplots_adjust(wspace=0)
    
    fig.text(.5, 0.025, 'Right Ascension (h)',
             horizontalalignment='center',
             verticalalignment='center',
             fontsize=20)
    py.savefig(os.path.join(_path,'Figures/fig3.png'))
    py.show()
    
if __name__ == '__main__':
    
    main(sys.argv)