#! /usr/bin/env python

'''
	Create pointing for SPLUS around the LMC and SMC.
'''

import numpy as np

def main():

	#      ra(deg)  dec(deg)  size (deg)
	LMC = [80.8942,	-69.7561, 11.]
	SMC = [13.2,-72.8, 11.]
	
	# size os field
	ancho=1.454

	LMC_ra = np.arange(LMC[0]-LMC[2]/2.,LMC[0]+LMC[2]/2.+ancho,ancho)
	LMC_dec = np.arange(LMC[1]-LMC[2]/2.,LMC[1]+LMC[2]/2.+ancho,ancho)

	SMC_ra = np.arange(SMC[0]-SMC[2]/2.,SMC[0]+SMC[2]/2.+ancho,ancho)
	SMC_dec = np.arange(SMC[1]-SMC[2]/2.,SMC[1]+SMC[2]/2.+ancho,ancho)

	for i in range(len(LMC_ra)):
		for j in range(len(LMC_dec)):
			print LMC_ra[i],LMC_dec[j]

if __name__ == '__main__':

	main()