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
	
	period_grid = np.append(np.arange(0.04,1,0.1),np.arange(1,10,0.25))
	
	ecdur_grid = [0.01,0.1] #np.arange(0.01,0.1,0.01)
	
	depth_grid = [0.1,1.0] #np.arange(0.1,1.0,0.1)
	
	snr_grid = np.arange(5,220,5)
	snrmean_grid = np.zeros(len(snr_grid))
	snrstd_grid = np.zeros(len(snr_grid))
	NLC = 1000

	modeldata = np.array([])

	nruns = len(period_grid)*len(ecdur_grid)*len(depth_grid)*len(snr_grid)
	logging.info('Total number of light curves: %i'%(nruns*NLC))

	# Generate 100 light curves for each
	
	std_1 = np.zeros(NLC*len(snr_grid)).reshape(len(snr_grid),NLC)
	std_2 = np.zeros(NLC)
	prop = np.zeros(len(snr_grid))
		
	pitr = int(argv[1])

	#for pitr in [0]: #range(len(period_grid)):

	for eitr in range(len(ecdur_grid)):
		for ditr in range(len(depth_grid)):
			prop = np.zeros(len(snr_grid))
			for itr,snr in enumerate(snr_grid):
				for ilc in range(NLC):
					tobs = np.array([17.0413348326,17.0480014993,26.1886086683,30.3348673002])+np.random.random(1)[0]*10-5
					flux = varModels.ecbinary(tobs,period_grid[pitr],ecdur_grid[eitr],depth_grid[ditr])
					ecerr = np.random.exponential(1./snr,len(tobs)) * (-1)**np.random.randint(0,2,len(tobs))
					std_1[itr][ilc] = np.std(flux+ecerr)
					std_2[ilc] = np.std(ecerr)

				snrmean_grid[itr] = np.mean(std_2)
				snrstd_grid[itr] = np.std(std_2)
				detect = std_1[itr] > snrmean_grid[itr]+3*snrstd_grid[itr]
				prop[itr] = float(len(std_1[itr][detect]))/float(len(std_1[itr]))
			logging.info('[%7i/%i] positions done. P = %.2f | Dur. = %.2f | Depth = %.2f'%(pitr*len(ecdur_grid)*len(depth_grid)+eitr*len(depth_grid)+ditr+1,nruns,period_grid[pitr],ecdur_grid[eitr],depth_grid[ditr]))
			modelinfo = {	'type'	: 'binary',
							'par'	: [period_grid[pitr],ecdur_grid[eitr],depth_grid[ditr]],
							'snr'	: snr_grid,
							'prop'	: prop}
			modeldata = np.append(modeldata,[modelinfo])

	logging.info('Saving data to binary_p%02i'%(pitr))
	np.save('binary_p%02i'%(pitr),modeldata)

	return 0

###################################################################################################

if __name__ == '__main__':

	logging.basicConfig(filename=sys.argv[0].replace('.py','_p%02i.log'%(int(sys.argv[1]))),
						level=logging.DEBUG,
						format='%(asctime)s %(message)s')

	main(sys.argv)