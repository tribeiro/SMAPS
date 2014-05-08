'''
Simulates scheduler operations for T80 South.
'''

import sys,os
import numpy as np
import _skysub
#from astropy.coordinates import ICRS
#from astropy import units as u

################################################################################

class SurveySim():

	############################################################################
	
	def __init__(self,ra,dec,ii,jj,ntrays,exptime):

		# Default observatory information
		self.sitelat = -30.228
		self.sitelong = 4.715
		# Default sun Max Alt (defines star/end of night)
		self.sunMaxAlt = -18.
		self.fullmoon = 0.95

		self.vfac = 0.65
		self.rvfac = 0.5
		
		# Store tiles coordinate information
		self._ii = np.array(ii)
		self._jj = np.array(jj)
		self._ra = np.array(ra)
		self._dec = np.array(dec)
		
		
		# Store maximum altitude of tiles
		self.maxAltit = []
		for i in range(ntrays):
			self.maxAltit.append(np.array([_skysub.altit(self._dec[i][j],0.,self.sitelat)[0] for j in range(len(ra[i]))]))

		if len(exptime) != ntrays:
			raise IOError('Number of trays/filters must match number of exposure times. ')

		self.ntrays = ntrays		# Number of trays/filters
		self.exptime = np.array(exptime)
		
		# Store which observation where performed or not
		self.obs = []
		for i in range(ntrays):
			self.obs.append(np.zeros(len(ii[i]))==0)
		
		# Store tiles to be repeated
		# tile - tile index
		# day  - day to be repeated
		# nrepeat - number of times to repeat
		# nobs - number of times tile was observed
		self.repeatInfo = {	'tile' : np.arange(len(self._ra)),
							'day' : np.zeros(len(self._ra)),
							'nobs' : np.zeros(len(self._ra),dtype=int)}
		self._repeatTray = 0
		self.rexptime = 0
		self._nrepeat = 0
		self._dTime = 0
		#self.repeatTile = np.array([])

	############################################################################

	def setupSPLUS(self,repeatTray,nrepeat,dTime,texp=0.):
		
		self._repeatTray = repeatTray
		self._nrepeat = nrepeat
		self._dTime = dTime

		self.repeatInfo = {	'tile' : np.arange(len(self._ra[repeatTray])),
							'day' : np.zeros(len(self._ra[repeatTray])),
							'nobs' : np.zeros(len(self._ra[repeatTray]),dtype=int)}

		if texp > 0:
			self.rexptime=texp
		else:
			self.rexptime=self.exptime[repeatTray]



	############################################################################

	def raMask(self,tray,lst_start,lst_end):

		ra_mask = []
		# Check ha
		if lst_start < lst_end:
			ra_mask = np.bitwise_and(self._ra[tray] > lst_start*360./24., self._ra[tray] < lst_end*360./24.)

		else:
			obsmask1 = self._ra[tray] > lst_start*360./24.
			obsmask2 = np.bitwise_and(self._ra[tray] > 0.,self._ra[tray] < lst_end*360./24.)
			ra_mask = np.bitwise_or(obsmask1,obsmask2)

		return ra_mask

	############################################################################

	def makeObs(self,T0,T1):
			
		time = T0
		hd = 1./24
		maskRep = []
		if self._nrepeat > 0:
			maskRep = np.bitwise_and(self.repeatInfo['day'] > 0,self.repeatInfo['nobs'] < self._nrepeat)
		else:
			maskRep = self.repeatInfo['day'] > 0

		info = ['Observations start @ JD = %12.2f'%T0,
				'Observations end   @ JD = %12.2f'%T1,
				'Total number of tiles: %5i'%self.nTiles(),
				'Tiles to observe: %5i'%(self.obsTiles()),
				'Tiles to repeate: %5i'%(len(maskRep[maskRep])) ]
		
		# count time spent observing each tray
		obsTime = np.zeros(self.ntrays+1)

		# Calculate moon for this night
		queue = []
		ramoon = 0.
		decmoon = 0.
		distmoon = 0.
		rasun = 0.
		decsun = 0.
		
		ramoon,decmoon,distmoon = _skysub.lpmoon(T0,self.sitelat,_skysub.lst(T0,self.sitelong))
		
		ill_frac=0.5*(1.-np.cos(_skysub.subtend(ramoon,decmoon,rasun,decsun)))
		
		fullmoon = False
		if ill_frac >= self.fullmoon:
			fullmoon = True
			info.append('Full moon (%5.1f)'%(ill_frac*100))
			obsTime[-1] = (T1-T0)
		else:
			info.append('Moon %5.1f       '%(ill_frac*100.))
		
		cra = -99
		cdec = -99
		
		while time < T1 and not fullmoon:
		
			obsDone = False
			tray = 0
			obsTile = -1
			# Trying the first tray

			while ( (not obsDone) and (0 <= tray < self.ntrays) ):
			
				# Local Sidereal time at start -2hours and end +2hours
				lst_start = _skysub.lst(time-2.*hd,self.sitelong)
				lst_end = _skysub.lst(time+self.exptime[tray]+2.*hd,self.sitelong)
				
				# Check if there is observation to be repeated this night.
				if self._nrepeat > 0:
					maskRep = np.bitwise_and(np.bitwise_and(self.repeatInfo['day'] > 0, self.repeatInfo['day'] <= time),self.repeatInfo['nobs'] < self._nrepeat)
				else:
					maskRep = np.bitwise_and(self.repeatInfo['day'] > 0, self.repeatInfo['day'] <= time)
				
				ra_mask = self.raMask(self._repeatTray,lst_start,lst_end)
				repeated = False
				
				if len(maskRep[maskRep]) > 0:
					ra_tmpmask = np.bitwise_and(ra_mask,maskRep)
					if ra_tmpmask.any():
						# make repeate observation
						index = np.arange(len(self._ra[self._repeatTray]))[ra_tmpmask]
						# Selecting highest in the sky at the center of the observation
						lst = _skysub.lst(time+self.exptime[self._repeatTray]/2.,self.sitelong)*360./24.
					
						ha = (lst - self._ra[self._repeatTray][ra_tmpmask])*24./360.
						alt = np.array([_skysub.altit(self._dec[self._repeatTray][j],ha[i],self.sitelat)[0] for i,j in enumerate(index)])
						if len(alt) == 0:
							info.append('[R] No observable tiles available...')
						else:
							stg = alt.argmax()
							if alt[stg] > self.maxAltit[self._repeatTray][index[stg]]*self.rvfac:
								info.append('[R] Observation complete...     ')
								self.repeatInfo['nobs'][index[stg]] += 1
								self.repeatInfo['day'][index[stg]] += self._dTime
								obsDone = True
								repeated = True
								tray = self._repeatTray
							else:
								info.append('[R] Object too low. Alt = %7.2f, Max Alt = %7.2f...                   '%(alt[stg],self.maxAltit[self._repeatTray][index[stg]]))

				ra_mask = self.raMask(tray,lst_start,lst_end)
				# Check if makes sense to continue
				if ra_mask.any() and not obsDone:

					info.append('Number of observable tiles %4i'%len(ra_mask[ra_mask]))
					
					index = np.arange(len(self._ra[tray]))[np.bitwise_and(ra_mask,self.obs[tray])]
					# Selecting highest in the sky at the center of the observation
					lst = _skysub.lst(time+self.exptime[tray]/2.,self.sitelong)*360./24.
				
					#lst = _skysub.lst(time,sitelong) #*360./24.
					ha = (lst - self._ra[tray][ra_mask])*24./360.
					alt = np.array([_skysub.altit(self._dec[tray][j],ha[i],self.sitelat)[0] for i,j in enumerate(index)])
					
					if len(alt) == 0:
						info.append('No observable tiles available...')
						# Go to next tray
						tray+=1
					else:
						#info.append(['Suitable tile available...'])
						stg = alt.argmax()
						if alt[stg] > self.maxAltit[tray][index[stg]]*self.vfac:
							info.append('Observation complete...     ')
							obsTile = index[stg]
							obsDone = True
							# check if needs to be repeated
							if tray == self._repeatTray and self.repeatInfo['nobs'][index[stg]] < self._nrepeat and self.repeatInfo['day'][index[stg]] < time:
								self.repeatInfo['day'][index[stg]] = time+self._dTime
							elif tray == self._repeatTray and self.repeatInfo['day'][index[stg]] < time and  self._nrepeat < 0:
								self.repeatInfo['day'][index[stg]] = time+self._dTime
						else:
							obsDone = False
							info.append('Object too low. Alt = %7.2f, Max Alt = %7.2f...                   '%(alt[stg],self.maxAltit[tray][index[stg]]*self.vfac))

							# Go to next tray
							tray+=1
				elif repeated:
					tray = -self._repeatTray
				else:
					tray = -1
					info.append('No tiles available...')

			tray = np.abs(tray)
			# Check if observation was performed and in which tray
			if obsDone:
				if repeated:
					obsTime[tray]+=self.rexptime
					time+=self.rexptime
				else:
					obsTime[tray]+=self.exptime[tray]
					time+=self.exptime[tray]
				self.obs[tray][obsTile] = False
				queue.append('TILE%05i %6.2f %+7.2f %16.6f %2i %8.3f'%(obsTile,self._ra[tray][obsTile],self._dec[tray][obsTile],time,tray,self.exptime[tray]))

			else:
				# Try one more time
				# See if there is any field to be repeated in the sky
				maskRep = self.repeatInfo['day'] > 0
				lst_start = _skysub.lst(time-3.*hd,self.sitelong)
				lst_end = _skysub.lst(time+self.rexptime+3.*hd,self.sitelong)
				ra_mask = self.raMask(self._repeatTray,lst_start,lst_end)
				repeated = False
				idx = 0
				if len(maskRep[maskRep]) > 0:
					ra_tmpmask = np.bitwise_and(ra_mask,maskRep)
					
					if ra_tmpmask.any():
						# make repeate observation
						index = np.arange(len(self._ra[self._repeatTray]))[ra_tmpmask]
						# Selecting highest in the sky at the center of the observation
						lst = _skysub.lst(time+self.exptime[self._repeatTray]/2.,self.sitelong)*360./24.
					
						ha = (lst - self._ra[self._repeatTray][ra_tmpmask])*24./360.
						alt = np.array([_skysub.altit(self._dec[self._repeatTray][j],ha[i],self.sitelat)[0] for i,j in enumerate(index)])
						if len(alt) == 0:
							info.append('[R] No observable tiles available...')
						else:
							stg = alt.argmax()
							if alt[stg] > self.maxAltit[self._repeatTray][index[stg]]*self.rvfac:
								info.append('[R] Observation complete...     ')
								self.repeatInfo['nobs'][index[stg]] += 1
								self.repeatInfo['day'][index[stg]] += self._dTime
								obsDone = True
								repeated = True
								tray = -self._repeatTray
								idx = index[stg]
							else:
								obsDone = False
								info.append('[R] Object too low. Alt = %7.2f, Max Alt = %7.2f [RR]...                   '%(alt[stg],self.maxAltit[self._repeatTray][index[stg]]*self.rvfac))
				if obsDone:
					obsTime[self._repeatTray] += self.rexptime
					time+=self.rexptime
				else:
					obsTime[-1] += self.exptime.max()
					time+=self.exptime.max()
		
		queueInfo = '%16.6f %6.3f '%(T0,(T1-T0)*24.)
		for tray in range(len(obsTime)):
			queueInfo += '%10.7f '%(obsTime[tray]*24.)
		return info,queue,queueInfo

	############################################################################

	def allDone(self):

		alldone = np.zeros(self.ntrays) == 1
		for i in range(self.ntrays):
			alldone[i] = self.obs[i].sum() == 0
		
		return alldone.any()

	############################################################################
	
	def nTiles(self,tray=-1):
		ntiles = 0
		if tray < 0:
			for i in range(len(self._ra)):
				ntiles += len(self._ra[i])
		else:
			ntiles = len(self._ra[tray])
		return ntiles

	############################################################################
	
	def obsTiles(self,tray=-1):
		ntiles = 0
		if tray < 0:
			for i in range(len(self._ra)):
				ntiles += len(self._ra[i][self.obs[i]])
		else:
			ntiles = len(self._ra[tray][self.obs[tray]])
		return ntiles

	############################################################################
	
	def Tiles(self):
		return len(self._ra)
		
	############################################################################

	def surveyImage(self):

		xx = self._ii.max()+1
		yy = self._jj.max()+1

		map = np.zeros(xx*yy).reshape(yy,xx)
		
		for i in range(len(self._ii)):
			map[self._jj[i]][self._ii[i]] = 1.0
		xmap = np.array([map]*self.ntrays)

		for iciclo in range(self.ntrays):
			xjj = self._jj[np.bitwise_not(self.obs[iciclo])]
			xii = self._ii[np.bitwise_not(self.obs[iciclo])]
			for i in range(len(xii)):
				xmap[iciclo][xjj[i]][xii[i]] = 2.0

		map = np.zeros(xx*yy).reshape(yy,xx)
		for i in range(self.ntrays):
			map+=xmap[i]
		map-=1
		return map

	############################################################################

	def trayImage(self,tray):

		xx = self._ii.max()+1
		yy = self._jj.max()+1

		map = np.zeros(xx*yy).reshape(yy,xx)
		
		for i in range(len(self._ii)):
			map[self._jj[i]][self._ii[i]] = 1.0

		xjj = self._jj[np.bitwise_not(self.obs[tray])]
		xii = self._ii[np.bitwise_not(self.obs[tray])]

		for i in range(len(xii)):
			map[xjj[i]][xii[i]] = 2.0
			
		if tray == self._repeatTray:
			maskRep = self.repeatInfo['nobs'] > 0
			idx = np.arange(len(maskRep))[maskRep]
			xjj = self._jj[maskRep]
			xii = self._ii[maskRep]
			
			for i in range(len(xii)):
				map[xjj[i]][xii[i]] += self.repeatInfo['nobs'][idx[i]]
		else:
			xjj = self._jj[np.bitwise_not(self.obs[tray])]
			xii = self._ii[np.bitwise_not(self.obs[tray])]

			for i in range(len(xii)):
				map[xjj[i]][xii[i]] = 2.0+self._nrepeat

		return map

	############################################################################
	'''
	def obsTiles(self,tray):

		rval = len(self.obs[tray][np.bitwise_not(self.obs[tray])])
		
		rval += np.sum(self.repeatInfo['nobs'])

		return rval
	'''
################################################################################