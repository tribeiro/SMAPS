import numpy as np
import pylab as py

def comp():
    ptall = np.loadtxt( '../coordinatesystemandtiling/all.dat',unpack=True)
    ptss = np.loadtxt( '../coordinatesystemandtiling/smaps_pointsulT80.dat',unpack=True)
    ptjn = np.loadtxt( 'norpointT80.dat',unpack=True)
    ptsn = np.loadtxt( '../coordinatesystemandtiling/smaps_pointT80norte.dat',unpack=True)
    ptjs = np.loadtxt( 'surpointT80.dat',unpack=True)

    print 'SMAPS: ', ptss.shape[1]+ptsn.shape[1]
    print 'J-PAS: ',ptjn.shape[1]+ptjs.shape[1]

    py.subplot(211)
    py.cla()
    py.plot(ptall[4],ptall[5],'g.')
    py.plot(ptjn[4],ptjn[5],'b.')
    py.plot(ptss[4],ptss[5],'r.')
    py.plot(ptjs[4],ptjs[5],'b.')
    py.plot(ptsn[4],ptsn[5],'r.')
    py.subplot(212)
    py.cla()
    py.plot(ptall[0],ptall[1],'g.')
    py.plot(ptjn[0],ptjn[1],'b.')
    py.plot(ptss[0],ptss[1],'r.')
    py.plot(ptjs[4],ptjs[5],'b.')
    py.plot(ptsn[4],ptsn[5],'r.')
    py.show()

if __name__ == '__main__':

    comp()
