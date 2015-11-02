import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("/Volumes/TiagoHD2/Documents/JPAS/x.py/F5.typeOnly.st",
				  dtype={'names': ('ocurrence', 'type'), \
				  'formats': ('i5', 'S5')})

plt.ioff()
'''
msptypes = np.array([tt[0] for tt in data['type']])
idx = 0
sptypes = ['O','B','A','F','G','K','M','L']
spt2int = np.zeros(len(sptypes))


for i in range(1,len(sptypes)):
	mask = msptypes == sptypes[i]
	idx+=len(msptypes[mask])
	spt2int[i] = idx
'''

mask = np.zeros(len(data['type']))+(-1)**np.arange(len(data['type'])) == 1
aran = np.arange(len(data['type']))[mask]
atypes = data['type'][mask]

mask = np.zeros(len(atypes))+(-1)**np.arange(len(aran)) == 1

plt.xticks(aran[mask],atypes[mask],rotation=90,verticalalignment='top')
plt.plot(data['ocurrence'])

nmask=np.bitwise_not(mask)
plt.twiny()
plt.xticks(aran[nmask],atypes[nmask],rotation=90,verticalalignment='top')
plt.plot(data['ocurrence'])

plt.show()
