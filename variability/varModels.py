
import numpy as np

###################################################################################################

def ecbinary(time,period,ecduration,depth):

	'''
	Simulate eclipsing binary.
	'''

	phase = time / period

	cycle = np.ceil(phase)

	phase = phase - cycle

	mask = np.bitwise_and(phase > -ecduration, phase < ecduration)

	flux = np.zeros_like(time)+1.0

	flux[mask] -= depth

	return flux


###################################################################################################

def pulsating(time,period,amplitude):

	'''
	Simulate pulsating star.
	'''

	return np.sin(2*np.pi*time/period)


###################################################################################################

def transient(time,t0,amplitude,duration):

	flux = np.zeros_like(time)

	mask = time > t0

	flux[mask] += amplitude * np.exp(- ((time[mask]-t0) / duration)**2.)

	return flux

###################################################################################################

###################################################################################################
if __name__ == '__main__':

	import pylab as py
	
	tt  = np.arange(10,40,0.1)
	#tobs = np.loadtxt(	'/Users/tiago/Documents/JPAS/variables/filtersObservations.txt',
	#					delimiter=',',unpack=True,usecols=(1,))
	
	mag0 = 16

	ectobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
	ectobs.sort()
	ecflx = mag0-ecbinary(tt,2,0.1,1.5)
	ecobs = mag0-ecbinary(ectobs,2,0.1,1.5)
	ecerr = np.random.exponential(0.1,len(ectobs)) * (-1)**np.random.randint(0,2,len(ectobs))

	pltobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
	pltobs.sort()

	plflx = mag0-pulsating(tt,2,0.5)
	plobs = mag0-pulsating(pltobs,2,0.5)
	plerr = np.random.exponential(0.1,len(pltobs)) * (-1)**np.random.randint(0,2,len(pltobs))

	trtobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
	trtobs.sort()

	trflx = mag0-transient(tt,20,1.0,10)+transient(tt,600,10.0,40)
	trobs = mag0-transient(trtobs,20,1.0,10)+transient(trtobs,600,10.0,40)
	trerr = np.random.exponential(0.1,len(trtobs)) * (-1)**np.random.randint(0,2,len(trtobs))
	
	py.figure(1,figsize=(8,4))
	########################
	
	ax1 = py.subplot(311)

	py.plot(tt,ecflx,'-')
	py.errorbar(ectobs,ecobs+ecerr,0.1,fmt='o')

	py.ylim(17.499,14.5)
	
	ax2 = py.subplot(312)

	py.plot(tt,plflx,'-')
	py.errorbar(pltobs,plobs+plerr,0.1,fmt='o')
	py.ylim(17.5,14.5)

	ax3 = py.subplot(313)

	py.plot(tt,trflx,'-')
	py.errorbar(trtobs,trobs+trerr,0.1,fmt='o')
	py.ylim(17.5,14.501)
	
	########################
	
	py.setp(ax1.get_xticklabels(),visible=False)
	py.setp(ax2.get_xticklabels(),visible=False)

	ax3.set_xlabel('Time (days)')
	ax2.set_ylabel('Magnitude')
	
	py.subplots_adjust(hspace=0,wspace=0,bottom=0.13,top=0.93)

	#py.savefig('/Users/tiago/Dropbox/Apps/TeX Writer (1)/fig/jpas_variability_fig01.pdf')

	py.show()

###################################################################################################