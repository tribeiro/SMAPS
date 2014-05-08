#!/usr/bin/env python

import sys,os
import numpy as np
import pylab as py
import varModels
import logging
###################################################################################################

def main(argv):

	# Defining grid of parameters for each model
	
	## Starting with eclipsing binaries
	
	### Periods in days from 1 hour to 10 days (the larger the orbital period the
	### to be an eclipse.
	
	period_grid = [2.] #np.append(np.arange(0.04,1,0.1),np.arange(1,10,0.25))
	
	amplitude_grid = [0.5] #np.arange(0.01,1.0,0.02)
	
	snr_grid = np.append(np.arange(5,15,1),np.arange(15,220+6,6))
	snrmean_grid = np.zeros(len(snr_grid))
	snrstd_grid = np.zeros(len(snr_grid))
	NLC = 1000

	modeldata = np.array([])

	nruns = len(period_grid)*len(amplitude_grid)*len(snr_grid)
	logging.info('Total number of light curves: %i'%(nruns*NLC))

	# Generate NLC light curves for each
	
	std_1 = np.zeros(NLC*len(snr_grid)).reshape(len(snr_grid),NLC)
	std_2 = np.zeros(NLC)
	prop = np.zeros(len(snr_grid))
		
	#for pitr in [0]: #range(len(period_grid)):

	for pitr in range(len(period_grid)):
		for aitr in range(len(amplitude_grid)):
			prop = np.zeros(len(snr_grid))
			for itr,snr in enumerate(snr_grid):
				for ilc in range(NLC):
					tobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
					flux = varModels.pulsating(tobs,period_grid[pitr],amplitude_grid[aitr])
					ecerr = np.random.exponential(1./snr,len(tobs)) * (-1)**np.random.randint(0,2,len(tobs))
					std_1[itr][ilc] = np.std(flux+ecerr)
					std_2[ilc] = np.std(ecerr)

				snrmean_grid[itr] = np.mean(std_2)
				snrstd_grid[itr] = np.std(std_2)
				detect = std_1[itr] > snrmean_grid[itr]+3*snrstd_grid[itr]
				prop[itr] = float(len(std_1[itr][detect]))/float(len(std_1[itr]))
			logging.info('[%7i/%i] positions done. P = %.2f | Amp = %.2f'%(pitr*len(amplitude_grid)+aitr,nruns,period_grid[pitr],amplitude_grid[aitr]))
			modelinfo = {	'type'	: 'pulsating',
							'par'	: [period_grid[pitr],amplitude_grid[aitr]],
							'snr'	: snr_grid,
							'prop'	: prop}
			modeldata = np.append(modeldata,[modelinfo])

	logging.info('Saving data to pulsating_p%02i'%(pitr))
	#np.save(os.path.expanduser('~/rdata/variability3/pulsating_p%02i'%(pitr)),modeldata)

	ax = py.subplot(211)
	for itr,snr in enumerate(snr_grid):
		detect = std_1[itr] > snrmean_grid[itr]+3*snrstd_grid[itr]
		py.plot(np.zeros(NLC)+snr,std_1[itr],'b.')
		py.plot(np.zeros(NLC)[detect]+snr,std_1[itr][detect],'bo')
		prop[itr] = float(len(std_1[itr][detect]))/float(len(std_1[itr]))

	#py.plot(1./snr_grid,1.4/snr_grid,'r-')
	py.plot(snr_grid,snrmean_grid+1*snrstd_grid,'g--')
	py.plot(snr_grid,snrmean_grid,'r-')
	py.plot(snr_grid,snrmean_grid-1*snrstd_grid,'g--')

	y1=snrmean_grid+3*snrstd_grid
	y2=snrmean_grid-3*snrstd_grid
	y2[y2 <0] = 0
	py.fill_between(snr_grid,
					y1,
					y2, color='green', alpha='0.5')
	
	py.ylabel('$\\sigma$')
	py.setp(ax.get_xticklabels(),visible=False)
	ylim = py.ylim()
	py.ylim(-0.1,ylim[1])

	py.subplot(212)
	py.plot(snr_grid,prop,'-')

	py.ylabel('Detectability')
	py.xlabel('S/N')

	py.show()

	return 0

###################################################################################################

if __name__ == '__main__':

	logging.basicConfig(filename=sys.argv[0].replace('.py','.log'),
						level=logging.INFO,
						format='%(asctime)s %(message)s')

	main(sys.argv)
