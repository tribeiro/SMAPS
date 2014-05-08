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
	
	decay_grid = np.append(np.arange(0.04,1,0.1),np.arange(1,10,0.25))
	
	amplitude_grid = np.arange(0.01,1.0,0.02)
	
	snr_grid = np.append(np.arange(5,15,1),np.arange(15,220+6,6))
	snrmean_grid = np.zeros(len(snr_grid))
	snrstd_grid = np.zeros(len(snr_grid))
	NLC = 1000

	modeldata = np.array([])

	nruns = len(decay_grid)*len(amplitude_grid)*len(snr_grid)
	logging.info('Total number of light curves: %i'%(nruns*NLC))

	# Generate NLC light curves for each
	
	std_1 = np.zeros(NLC*len(snr_grid)).reshape(len(snr_grid),NLC)
	std_2 = np.zeros(NLC)
	prop = np.zeros(len(snr_grid))
		
	#for pitr in [0]: #range(len(period_grid)):

	for pitr in range(len(decay_grid)):
		for aitr in range(len(amplitude_grid)):
			prop = np.zeros(len(snr_grid))
			for itr,snr in enumerate(snr_grid):
				for ilc in range(NLC):
					tobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
					flux = varModels.transient(tobs,20,decay_grid[pitr],amplitude_grid[aitr])
					ecerr = np.random.exponential(1./snr,len(tobs)) * (-1)**np.random.randint(0,2,len(tobs))
					std_1[itr][ilc] = np.std(flux+ecerr)
					std_2[ilc] = np.std(ecerr)

				snrmean_grid[itr] = np.mean(std_2)
				snrstd_grid[itr] = np.std(std_2)
				detect = std_1[itr] > snrmean_grid[itr]+3*snrstd_grid[itr]
				prop[itr] = float(len(std_1[itr][detect]))/float(len(std_1[itr]))
			logging.info('[%7i/%i] positions done. P = %.2f | Amp = %.2f'%(pitr*len(amplitude_grid)+aitr,nruns,decay_grid[pitr],amplitude_grid[aitr]))
			modelinfo = {	'type'	: 'pulsating',
							'par'	: [decay_grid[pitr],amplitude_grid[aitr]],
							'snr'	: snr_grid,
							'prop'	: prop}
			modeldata = np.append(modeldata,[modelinfo])

	logging.info('Saving data to transients_p%02i'%(pitr))
	np.save(os.path.expanduser('~/rdata/variability3/transients_p%02i'%(pitr)),modeldata)

	return 0

###################################################################################################

if __name__ == '__main__':

	logging.basicConfig(filename=sys.argv[0].replace('.py','.log'),
						level=logging.INFO,
						format='%(asctime)s %(message)s')

	main(sys.argv)
