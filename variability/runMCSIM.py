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
	
	ecdur_grid = np.arange(0.01,0.1,0.01)
	
	depth_grid = np.arange(0.1,1.0,0.1)
	
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
		
	_pitr = [0]
	_eitr = [0]
	_ditr = [len(depth_grid)-1]
		
	for pitr in [0]: #range(len(period_grid)):
		for eitr in [0]: #range(len(ecdur_grid)):
			for ditr in [len(depth_grid)-1]: #range(len(depth_grid)):
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

	logging.info('Saving data to binary.npy')
	np.save('binary',modeldata)

	#return 0

	py.subplot(211)
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

	py.subplot(212)
	py.plot(snr_grid,prop,'-')

	py.show()
			
	return 0

###################################################################################################

if __name__ == '__main__':

	logging.basicConfig(filename=sys.argv[0].replace('.py','.log'),
						level=logging.INFO,
						format='%(asctime)s %(message)s')

	main(sys.argv)