
import os
import ConfigParser

import numpy as np

from chimera.core.chimeraobject import ChimeraObject
from chimera.core.cli import ChimeraCLI, action
from chimera.core.manager import Manager
from chimera.util.position import Position

from chimera.controllers.scheduler.model import (Session, Targets, Program, Point,
                                                 Expose, PointVerify, AutoFocus, Projects)

from chimera.core.systemconfig import SystemConfig
from chimera.core.site import (Site, datetimeFromJD)

import re

try:
	import _skysub
except ImportError:
	print '''To load chimera's TAO interface you need skycalc instaled. Skycalc can be downloaded at ().'''

cfgpath = os.path.dirname(__file__)

####################################################################################################################################

class MKQueue (ChimeraObject):
	'''
	A queue maker that operates with chimera for automated scheduling of observations. The input target lists are loaded
	as configuration files and individual targets for different projects can be separated with individual flags. These flags
	can then be used to apply different scheduling algorithms.
	
	Current algorithms are:
	
	1 - Standard stars:
	
		Observe a 'user defined' number of standard stars at a 'user defined' number of different airmasses throughout the night.

	2 - Lower airmass with specific conditions:
	
		Fill the night, or a 'user defined' portion of the night, with targets to be observed at the lower airmass as possible
		with a superior limit on airmass. 
		
		Available filters are:
			- Exposure time per filter
			- Moon: Filter selection based on moon brightness
			- Weather constraints: Seeing and Cloud cover.
		
		
	'''
	
	schedInfo = {	'targetFlag'					: '', # Main info
					'targetschedAlgorith'			: -1,
					'targetFilter'					: '',
					'targetExpTime'					: -1,
					'targetMaxAirmass'				: 1.8,
					'targetMaxMoonBright'			: 100.,
					'targetMinMoonBright'			: 0.,
					'targetMinMoonDist'				: 0.,
					'targetMaxSeeing'				: 1.8,
					'targetCloudCover'				: 0}
					
#					'sunMaxAlt'						: -18.}

	####################################################################################################################################
	
	def __init__(self):
		'''
		Constructor.
		'''
        
		ChimeraObject.__init__(self)
		self.sunMaxAlt = -18.
		self.isJD = False
		self.tbin = 1./60./24. # Default time bin is 1 minute.
		self.tolairmass = 0.01
		

	####################################################################################################################################
	
#	def __start__(self):
#
#		site=Site()
#		nowmjd=site.MJD()
#		self.setJD(nowmjd+2400000.5)
#		self.selectStandardTargets()
#		self.selectScienceTargets()

		
	####################################################################################################################################
	
	def setJD(self,options):
		'''
		Configure time domain by specifing a julian day. It will use information on exposure time to build time bins that will be 
		filled when selecting targets.
		'''
		
		sysconfig = SystemConfig.fromFile(options.config)

		manager = Manager()
		site = manager.getProxy(sysconfig.sites[0])
		jd = options.JD
		
		if not jd:
			jd = np.floor(site.JD())+0.5
		
		lat = np.array([float(tt) / 60.**i for i,tt in enumerate(str(site['latitude']).split(':'))])
		lat[1:] *= lat[0]/np.abs(lat[0])
		sitelat = np.sum(lat)
		long = np.array([float(tt) / 60.**i for i,tt in enumerate(str(site['longitude']).split(':'))])
		long[1:] *= long[0]/np.abs(long[0])
		sitelong = abs(np.sum(long)/360*24.)
		
		print site['latitude'],'->',sitelat
		print site['longitude'],'->',sitelong
		
		nightstart = _skysub.jd_sun_alt(self.sunMaxAlt, jd, sitelat, sitelong)
		nightend   = _skysub.jd_sun_alt(self.sunMaxAlt, jd+0.5, sitelat, sitelong)
		print('Nigh Start @JD= %.3f # Night End @JD = %.3f'%(nightstart,nightend))

		
		# Creating a 1 minute time bin
		tbin = self.tbin

		self.obsTimeBins = np.arange(nightstart,nightend+tbin,tbin)
		self.obsTimeMask = np.zeros(len(self.obsTimeBins))
		self.obsTimeMask[-1] = 1.0
		
		# Marking filled bins
		
		session = Session()
		
		scheduled = session.query(Program)
		
		for target in scheduled:
			tindex = np.abs(self.obsTimeBins - 2400000.5 - target.slewAt).argmin()
			self.obsTimeMask[tindex] = 1.0

		self.isJD = True

	####################################################################################################################################

	def selectScienceTargets(self):
		'''
		Based on configuration parameters select a good set of targets to run scheduler on a specified Julian Day.
		'''
		
		session = Session()
		
		# [To be done] Reject objects that are close to the moon

		for tbin,time in enumerate(self.obsTimeBins):

			if self.obsTimeMask[tbin] < 1.0:
				# Select objects from database that where not observed and where not scheduled yet
				# In the future may include targets that where observed a number of nights ago.
				# This is still incomplete. We should also consider the distance from the previous pointing to the next!
				# Since a target can have a higher airmass but be farther away from a neaby target that will take less time
				# to point.
				# one way of selecting targets that are close together and have good airmass is to select regions that are close
				# to the current location. it can start as searching an area with r1 ~ 10 x the FoV and, if there are no regions
				# to to x2 that and then x4 that. If still there are no targets, than search for the higher in the sky.
				targets = session.query(Targets).filter(Targets.observed == False).filter(Targets.scheduled == False).filter(Targets.type == self.sciFlag)
			
				lst = _skysub.lst(time,self.sitelong) #*360./24.
				alt = np.array([_skysub.altit(target.targetDec,lst - target.targetRa,self.sitelat)[0] for target in targets])
				stg = alt.argmax()

				self.log.info('Selecting %s'%(targets[stg]))
				
				# Marking target as schedule
				tst = session.query(Targets).filter(Targets.id == targets[stg].id)

				for t in tst:
					t.scheduled = True
					session.commit()
					self.addObservation(t,time)
				
				self.obsTimeMask[tbin] = 1.0
			else:
				self.log.debug('Bin %3i @mjd=%.3f already filled up with observations. Skipping...'%(tbin,time-2400000.5))
				
		#print i
		return 0 #targets

	####################################################################################################################################

	def selectStandardTargets(self,flag,nstars=3,nairmass=3):
		'''
		Based on configuration parameters, select 'nstars' standard stars to run scheduler on a specified Julian Day. Ideally you 
		will select standard stars before your science targets so not to have a full queue. Usually standard stars are observed 
		more than once a night at different airmasses. The user can control this parameter with nairmass and the script will try
		to take care of the rest. 
		'''

		session = Session()
		
		# query project information
		projQuery = session.query(Projects).filter(Projects.flag == flag)
		
		totobstime = 0.
		
		# Calculate total observation time
		
		for block in projQuery:
			totobstime += block.exptime
		totobstime /= 86400.0
		# First of all, standard stars can be observed multiple times in sucessive nights. I will mark all
		# stars as unscheduled.
		
		targets = session.query(Targets).filter(Targets.scheduled == True).filter(Targets.type == flag)
		for target in targets:
			target.scheduled = False
			session.commit()
		
		# [To be done] Reject objects that are close to the moon
		# [To be done] Apply all sorts of rejections

		# Selecting standard stars is not only searching for the higher in that time but select stars than can be observed at 3
		# or more (nairmass) different airmasses. It is also important to select stars with different colors (but this will be
		# taken care in the future).

		if nairmass*nstars > len(self.obsTimeBins):
			self.log.warning('Requesting more stars/observations than it will be possible to schedule. Decreasing number of requests to fit in the night.')
			nstars = len(self.obsTimeBins)/nairmass


		# Build a grid of desired times for higher airmass observation of each standard star.
		
		stdObsTimeBin = np.arange(10,len(self.obsTimeBins)-10,(len(self.obsTimeBins)-10)/nstars)
		obsStandars = np.zeros(nstars)
		print stdObsTimeBin
		
		# selecting the closest bin without observation

		stdObsTimeBin,status = self.findSuitableTimeBin(stdObsTimeBin)
		
		if status != 0:
			raise Exception('Could not find suitable time to start observations! Try cleaning queue.')
			
		print stdObsTimeBin
		
		site = Site()

		calclst = lambda time: np.sum(np.array([float(tt) / 60.**i for i,tt in enumerate(str(site._getEphem(datetimeFromJD(time)).sidereal_time()).split(':'))]))
		nightlst = np.array([calclst(obstime) for obstime in self.obsTimeBins])


		for i,tbin in enumerate(stdObsTimeBin):
		
			# selecting the closest bin without observation
			closestcleanbin = tbin
			while self.obsTimeMask[closestcleanbin] > 0.0:
				closestcleanbin += 1
			if i+1 < len(stdObsTimeBin):
				if closestcleanbin > stdObsTimeBin[i+1]:
					raise Exception('Could not find suitable place to start observations of standard star. Try cleaning queue.')
			
			time = self.obsTimeBins[closestcleanbin]

			# 1 - Select objects from database that where not scheduled yet (standard stars may be repited)
			#     that fits our observing night

			#targetSched = False

			# Will try until a good match is obtained
			#while( not targetSched ):
			targets = session.query(Targets).filter(Targets.scheduled == 0).filter(Targets.type == flag)
			if len(targets[:]) > 0:

				#ephem = site._getEphem(datetimeFromJD(time))
				
				lst = calclst(time) #np.sum(np.array([float(tt) / 60.**i for i,tt in enumerate(str(ephem.sidereal_time()).split(':'))]))
				sitelat = np.sum(np.array([float(tt) / 60.**i for i,tt in enumerate(str(site['latitude']).split(':'))]))
				alt = np.array([_skysub.altit(target.targetDec,lst - target.targetRa,sitelat)[0] for target in targets])
				
				stg = alt.argmax()

				print('Selecting %s'%(targets[stg]))
				
				# Marking target as schedule
				tst = session.query(Targets).filter(Targets.id == targets[stg].id)
				
				# Build airmass table for object
				objsecz = np.array([_skysub.true_airmass(_skysub.secant_z(_skysub.altit(targets[stg].targetDec,nlst - targets[stg].targetRa,sitelat)[0])) for nlst in nightlst])
				# Build desired airmass table
				#obsairmass = np.linspace(_skysub.true_airmass(_skysub.secant_z(alt[stg])),projQuery[0].maxairmass,nairmass)
				obsairmass = np.logspace(np.log10(np.min(objsecz[objsecz > 0])),np.log10(projQuery[0].maxairmass),nairmass)
				np.savetxt('airmass_%04i.dat'%(stg),X=zip(self.obsTimeBins,objsecz))
				# Build mask with scheduled airmasses
				#mask = np.zeros(len(objsecz),dtype=bool) == 1
				pltobstime,pltobsairmass = np.array([]),np.array([])
				# Try scheduling observations on all airmasses
				for airmass in obsairmass:
				
					# Get times where the object is close to the desired airmass and there are no observations scheduled
					timeobsmask = np.bitwise_and(self.obsTimeMask < 1.0,np.abs(objsecz - airmass) < self.tolairmass)
					# Check that there are times available
					if not timeobsmask.any():
						#raise Exception('No time available for scheduling observations of standard star %s at airmass %.3f'%(targets[stg],airmass))
						self.log.warning('No time available for scheduling observations of standard star %s at airmass %.3f'%(targets[stg],airmass))
					# Start trying to schedule observations
					indexes = np.arange(len(self.obsTimeMask))[timeobsmask] #np.bitwise_and(self.obsTimeMask, timeobsmask)
					
					obsSched = False


					
					for index in indexes:
						print('[%.3f] - Time bin available for observation of standard star at airmass %.3f'%(self.obsTimeBins[index], airmass))
						print '- Require %i extra time bins'%(totobstime/self.tbin)
						if (self.obsTimeMask[index:index+totobstime/self.tbin] < 1.0).all():
							print 'Observation fit in this block.'
							self.obsTimeMask[index:index+totobstime/self.tbin] = 1.0
							self.log.info('Requesting observations of %s @airmass=%4.2f @mjd=%.3f...'%(target.name,airmass,self.obsTimeBins[index]-2400000.5))
							
							pltobstime = np.append(pltobstime,self.obsTimeBins[index:index+totobstime/self.tbin])
							pltobsairmass = np.append(pltobsairmass, objsecz[index:index+totobstime/self.tbin])
							

							#for nblock,ii in enumerate(range(index,int(index+totobstime/self.tbin),1)):
							self.addObservation(targets[stg],self.obsTimeBins[index],projQuery)
							break
					np.savetxt('obsairmass_%04i.dat'%stg,X = zip(pltobstime,pltobsairmass))

						#self.obsTimeMask[index] = 1.0
						#for iobsbins in range(index+1,index+int(totobstime/self.tbin)):
							#print '[%i] - require extra time bin'%(iobsbins)
							#if self.obsTimeMask[iobsbins] < 1.0:
							#	self.obsTimeMask[iobsbins] = 1.0
							#else:
							#	raise Exception('Time bin [%i/%i] not available for observation of standard star at airmass %.3f'%(iobsbins,len(self.obsTimeMask),airmass))
						#else:
							#raise Exception('Time bin not available for observation of standard star at airmass %.3f'%(airmass))

				for t in tst:
					t.scheduled = True
					session.commit()
					obsStandars[i] = t.id
			else:
				self.log.warning('No suitable standard star for jd:%.3f in database...'%(time))
				return 0

		return 0
		
		if len(obsStandars[obsStandars >= 0]) < nstars:
			self.log.warning('Could not find %i suitable standard stars in catalog. Only %i where found.'%(nstars,len(obsStandars[obsStandars >= 0])))

		obsStandars = np.zeros(len(self.obsTimeBins))-1 # first selection of observable standards
		
		for tbin,time in enumerate(self.obsTimeBins):

			if self.obsTimeMask[tbin] < 1.0:
				# 1 - Select objects from database that where not scheduled yet (standard stars may be repited)
				#     that fits our observing night
				targets = session.query(Targets).filter(Targets.scheduled == 0).filter(Targets.type == flag)
				
				if len(targets[:]) > 0:

					ephem = site._getEphem(datetimeFromJD(time))
					
					lst = np.sum(np.array([float(tt) / 60.**i for i,tt in enumerate(str(ephem.sidereal_time()).split(':'))]))
					sitelat = np.sum(np.array([float(tt) / 60.**i for i,tt in enumerate(str(site['latitude']).split(':'))]))
					secz = np.array([_skysub.secant_z(_skysub.altit(target.targetDec,lst - target.targetRa,sitelat)[0]) for target in targets])
					
					stg = secz.argmax()

					self.log.info('Selecting %s'%(targets[stg]))
					
					# Marking target as schedule
					tst = session.query(Targets).filter(Targets.id == targets[stg].id)

					for t in tst:
						t.scheduled = True
						session.commit()
						obsStandars[tbin] = t.id
				else:
					print('No suitable target for jd:%.3f in database...'%(time))
					break

			else:
				self.log.info('Bin already filled up with observations. Skipping...')

		if len(obsStandars[obsStandars >= 0]) < nstars:
			self.log.warning('Could not find %i suitable standard stars in catalog. Only %i where found.'%(nstars,len(obsStandars[obsStandars >= 0])))
		#
		# Unmarking potential targets as scheduled
		#
		for id in obsStandars[obsStandars >= 0]:
			target = session.query(Targets).filter(Targets.id == id)
			for t in target:
				t.scheduled = False
				session.commit()
				
			tbin+=1
		#
		# Preparing a grid of altitudes for each target for each observing window
		#
		amGrid = np.zeros(len(obsStandars)*len(obsStandars)).reshape(len(obsStandars),len(obsStandars))

		for i in np.arange(len(obsStandars))[obsStandars >= 0]:
			target = session.query(Targets).filter(Targets.id == obsStandars[i])[0]
			for j in range(len(obsStandars)):
				lst = _skysub.lst(self.obsTimeBins[j],self.sitelong)
				amGrid[i][j] = _skysub.true_airmass(_skysub.secant_z(_skysub.altit(target.targetDec,lst - target.targetRa,self.sitelat)[0]))
				if amGrid[i][j] < 0:
					amGrid [i][j] = 99.
		#
		# Build a grid mask that specifies the position in time each target should be observed. This means that, when
		# selecting a single target we ocuppy more than one, non consecutive, position in the night. This grid shows where are these
		# positions.
		#
		obsMask = np.zeros(len(obsStandars)*len(obsStandars),dtype=np.bool).reshape(len(obsStandars),len(obsStandars))

		for i in np.arange(len(obsStandars))[obsStandars >= 0]:
			amObs = np.linspace(amGrid[i].min(),self.stdMaxAirmass,nairmass) # requested aimasses
			dam = np.mean(np.abs(amGrid[i][amGrid[i]<self.stdMaxAirmass][1:] - amGrid[i][amGrid[i]<self.stdMaxAirmass][:-1])) # how much airmass changes in average
			for j,am in enumerate(amObs):
				# Mark positions where target is at	specified airmass
				if j == 0:
					obsMask[i] = np.bitwise_or(obsMask[i],amGrid[i] == am)
				else:
					obsMask[i] = np.bitwise_or(obsMask[i],np.bitwise_and(amGrid[i]>am-dam,amGrid[i]<am+dam))

			#print amGrid[i][np.where(obsMask[i])]
		#
		# Now it is time to actually select the targets. It will start with the first target and then try the others
		# until it find enough standard stars, as specified by the user.
		#
		# Para cada bin em tempo, varro o bin em massa de ar por coisas observaveis. Se acho um, vejo se posso agendar
		# os outros bins. Se sim, marco o alvo para observacao, se nao, passo para o proximo. Repito ate completar a
		# lista de alvos
		#

		obsMaskTimeGrid = np.zeros(len(obsStandars),dtype=np.bool)
		nrequests = 0
		reqId = np.zeros(nstars,dtype=np.int)-1
		for tbin,time in enumerate(self.obsTimeBins[:-1]):
			# Evaluates if time slots are all available. If yes, mark orbservation and ocuppy slots.
			if ( (not obsMaskTimeGrid[obsMask[tbin]].any()) and (len(amGrid[tbin][obsMask[tbin]])>=nairmass) ):
				obsMaskTimeGrid = np.bitwise_or(obsMaskTimeGrid,obsMask[tbin])
				reqId[nrequests] = tbin
				nrequests += 1
			if nrequests >= nstars:
				break

		# Finally, requesting observations

		for id in reqId[reqId >= 0]:
			target = session.query(Targets).filter(Targets.id == obsStandars[id])[0]
			secz = amGrid[id][obsMask[id]]
			seczreq = np.zeros(nairmass,dtype=np.bool)
			amObs = np.linspace(amGrid[id].min(),self.stdMaxAirmass,nairmass) # requested aimasses
			for i,obstime in enumerate(self.obsTimeBins[obsMask[id]]):
				sindex = np.abs(amObs-secz[i]).argmin()
				if not seczreq[sindex]:
					self.log.info('Requesting observations of %s @airmass=%4.2f @mjd=%.3f...'%(target.name,secz[i],obstime-2400000.5))
					seczreq[sindex] = True
					target.scheduled = True
					session.commit()
					self.addObservation(target,obstime)
					self.obsTimeMask[obsMask[id]] = 1.0
			#print self.obsTimeBins[obsMask[id]]
			#print

		#print i
		return 0 #targets

	####################################################################################################################################

	def findSuitableTimeBin(self,timebins,maxtries=10):

		for i in range(len(timebins)):
			ntries = 0
			while self.obsTimeMask[timebins[i]] > 0.0:
				timebins[i] += 1
				ntries += 1
				if ntries > maxtries:
					return timebins, -1
		return timebins,0

	####################################################################################################################################

	def addObservation(self,target,obstime,blocks):
	
		session = Session()
		
		lineRe = re.compile('(?P<coord>(?P<ra>[\d:-]+)\s+(?P<dec>\+?[\d:-]+)\s+(?P<epoch>[\dnowNOWJjBb\.]+)\s+)?(?P<imagetype>[\w]+)'
                            '\s+(?P<objname>\'([^\\n\'\\\\]|\\\\.)*\'|"([^\\n"\\\\]|\\\\.)*"|([^ \\n"\\\\]|\\\\.)*)\s+(?P<exposures>[\w\d\s:\*\(\),]*)')
		programs = []
		
		entryFormat = '%(ra)s %(dec)s %(epoch)s %(obstype)s %(name)s %(exposures)s'
		
		p = Position.fromRaDec(target.targetRa,target.targetDec)
		ra = p.ra.HMS
		dec = p.dec.DMS
		
		filterExpt = [block.exptime for block in blocks]
		#if target.type == self.stdFlag:
		#	filterExpt = self.stdExpTime

		exposures = '1*('

		for i ,filter in enumerate([block.filter for block in blocks]):
			exposures = exposures+'%s:%.0f, '%(filter,filterExpt[i])


		exposures = exposures[:-2]
		exposures += ')'

		print exposures
				
		infos = {	'ra' : '%02.0f:%02.0f:%02.0f'%(ra[1],ra[2],ra[3]),
					'dec': '%+03.0f:%02.0f:%02.0f'%(dec[0]*dec[1],dec[2],dec[3]),
					'epoch' : 'J%.0f'%target.targetEpoch,
					'obstype' : 'OBJECT',
					'name' :target.name,
					'exposures' : exposures
					}

		i = 0
		line = entryFormat%infos
		
		matchs = lineRe.search(line)
		params = matchs.groupdict()
		
		position = None
		objname  = None

		if params.get("coord", None):
			position  = Position.fromRaDec(str(params['ra']), str(params['dec']), params['epoch'])

		imagetype = params['imagetype'].upper()
		objname   = params['objname'].replace("\"", "")

		multiplier, exps = params['exposures'].split("*")
		try:
			multiplier = int(multiplier)
		except ValueError:
			multiplier = 1

		exps = exps.replace("(", "").replace(")", "").strip().split(",")

		mjd = obstime - 2400000.5
		for i in range(multiplier):

			program = Program(tid = target.id ,name="%s-%03d" % (objname.replace(" ", ""), i),
                              slewAt=mjd,exposeAt=mjd+1./60./24.)

			self.log.info("# program: %s" % program.name)

			if imagetype == "OBJECT":
				if position:
					program.actions.append(Point(targetRaDec=position))
				else:
					program.actions.append(Point(targetName=objname))

			if imagetype == "FLAT":
				site = self._remoteManager.getProxy("/Site/0")
				flatPosition = Position.fromAltAz(site['flat_alt'], site['flat_az'])
				program.actions.append(Point(targetAltAz=flatPosition))

			#if i == 0:
			#    program.actions.append(AutoFocus(start=1500, end=3000, step=250, filter="R", exptime=10))
			#    program.actions.append(PointVerify(here=True))

			for exp in exps:
				if exp.count(":") > 1:
					filter, exptime, frames = exp.strip().split(":")
				else:
					filter, exptime = exp.strip().split(":")
					frames = 1

				if imagetype in ("OBJECT", "FLAT"):
					shutter = "OPEN"
				else:
					shutter = "CLOSE"

				if imagetype == "BIAS":
					exptime = 0

				if imagetype in ("BIAS", "DARK"):
					filter = None

				self.log.info("%s %s %s filter=%s exptime=%s frames=%s" % (imagetype, objname, str(position), filter, exptime, frames))

				program.actions.append(Expose(shutter=shutter,
											  filename="%s-$DATE-$TIME" % objname.replace(" ", ""),
											  filter=filter,
											  frames=frames,
											  exptime=exptime,
											  imageType=imagetype,
											  objectName=objname))
			self.log.info("")
			programs.append(program)

		session.add_all(programs)
		session.commit()
