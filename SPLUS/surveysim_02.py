#! /usr/bin/env python

'''
Simulates scheduler operations for T80 South.
'''

import sys,os
import numpy as np
import _skysub
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab
import matplotlib.pyplot as plt
from matplotlib import colors
import Image
import curses
import auxiliar as aux
import traceback

sitelat = -30.228
sitelong = 4.715
sunMaxAlt = -18.

def make_obs(T0,T1,RA,DEC,mask,texp,MaxAltit,obsTimes=[]):

	#obsmask = np.array(mask)
	
	i = 0
	
	lst_start = _skysub.lst(T0,sitelong)
	lst_end = _skysub.lst(T1,sitelong)
	ra_mask = []
	
	if lst_start < lst_end:
		ra_mask = np.bitwise_and(RA > lst_start*360./24., RA < lst_end*360./24.)
		stdscr.addstr(8,0,'[%5i] >> lst_start < lst_end <<'%(len(ra_mask[ra_mask])))
		stdscr.addstr(9,0,'                                 ')

	else:
		obsmask1 = RA > lst_start*360./24.
		obsmask2 = np.bitwise_and(RA > 0.,RA < lst_end*360./24.)
		ra_mask = np.bitwise_or(obsmask1,obsmask2)
		stdscr.addstr(8,0,'                                 ')
		stdscr.addstr(9,0,'[%5i] << lst_start > lst_end >>'%(len(ra_mask[ra_mask])))

	stdscr.refresh()
	obsmask = np.bitwise_and(mask,ra_mask)
	xindex = np.arange(len(RA))
	#stdscr.addstr(5,0,'%i %i'%(len(index[obsmask]),len(index[ra_mask])))
	stdscr.addstr(5,0,'Initial size of array %i'%(len(xindex)))
	ondex = []
	index = list(np.array(xindex)[obsmask])

	if len(obsTimes) == 0:
		_obsTimes = np.arange(T0,T1,texp)
	else:
		_obsTimes = obsTimes
	obsSlot = np.zeros_like(_obsTimes) == 1

	if len(index)>len(xindex[ra_mask]):
		stdscr.addstr(6,0,'[WARNING] More tiles available than it is possible!')
		stdscr.refresh()
		return mask,0,len(np.arange(T0,T1,texp)),_obsTimes

	if len(index) < 1:
		stdscr.addstr(6,0,'Nothing to observe...                                               ')
		stdscr.refresh()
		return mask,0,len(np.arange(T0,T1,texp)),_obsTimes
	__strlen = len('Running size of array %4i'%(len(index)))
	stdscr.addstr(6,0,'Running size of array %4i'%(len(index)))
	stdscr.refresh()
	#obsmask[ra_mask] = True
	#return obsmask,i
	#fp = open('queue_%05.0f.txt'%(T0-2400000.5),'w')
	for line in range(10):
		stdscr.addstr(10+line,0,'                                                                 ')

	line = 0

	for itr,time in enumerate(_obsTimes):
		
		lst = _skysub.lst(time,sitelong)*360./24.
	
		#lst = _skysub.lst(time,sitelong) #*360./24.
		ha = (lst - RA)*24./360.
		alt = np.array([_skysub.altit(DEC[j],ha[j],sitelat)[0] for j in index])
		if len(alt) == 0:
			stdscr.addstr(6,0,'Nothing to observe...                              ')
			stdscr.refresh()
		else:
			stg = alt.argmax()
			i+=1
			#stdscr.addstr(8,0,'%i %i %i'%(obsmask[index[stg]],index[stg],stg))
			if alt[stg] > MaxAltit[index[stg]]*0.6:
				ondex.append(index[stg])
				index.pop(stg)
				obsSlot[itr] = True
			else:
				stdscr.addstr(10+line,0,'Object too low. Alt = %7.2f, Max Alt = %7.2f...                   '%(alt[stg],MaxAltit[index[stg]]))
				if line < 9:
					line+=1
				stdscr.refresh()
		#stg = ha.argmin()
		
		#fp.write('tile%05i %f %f\n'%(	index[stg],
		#								RA[index[stg]],
		#								DEC[index[stg]]))
										

		#
		#xtime.sleep(1.0)
		
	#fp.close()
	obsmask = np.array(mask)
	for idx in ondex:
		if obsmask[idx] == False:
			stdscr.addstr(10,0,'[WARINING] - Tile repeated!')
			stdscr.refresh()
		obsmask[idx] = False
	#stdscr.addstr(8,0,'%i'%(len(xindex[mask])-len(xindex[obsmask])))
	stdscr.refresh()
	#print i
	return obsmask,len(ondex),len(_obsTimes),_obsTimes[obsSlot]
	#lun_age

################################################################################
#

def main(argv):

	'''
	Main function. Reads input parameters, run scheduler and stores results.
	'''

	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option("-s",'--south_pt',
                      help='''
Input file. This file contains the ra dec for all the tiles. The format is the 
same as the output of tiler.'''
					  ,type="string")
	parser.add_option("-n",'--north_pt',
                      help='''
Input file. This file contains the ra dec for all the tiles. The format is the 
same as the output of tiler.'''
					  ,type="string")

	parser.add_option("-m",'--meteorology',
                      help='''
Input file. This file contains weather information. Only clouded nights need be 
specified. Format is MJD FLAG, where FLAG is 
0 - Good night. Less than 0.5 mag extinction (may be skipped)
1 - Thin Cirrus. Between 0.5 and 2 mag extinction.
2 - Cloudy. Between 2 and 4 mag extinction.
3 - Closed.'''
					  ,type="string")
	parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")
    
	opt,arg = parser.parse_args(argv)
			
	#
	# Reading input files
	#

	_path = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/')

	sna_file = os.path.join(_path,'smaps_pointT80norte.dat')
	ssa_file = os.path.join(_path,'smaps_pointsulT80.dat')

	iis,jjs,ras,decs,rots = np.loadtxt(sna_file,unpack=True,usecols=(0,1,4,5,6))
	
	iin,jjn,ran,decn,rotn = np.loadtxt(ssa_file,unpack=True,usecols=(0,1,4,5,6))
	
	ii = np.array(np.append(iis,iin+iis.max()+10),dtype=int)
	jj = np.array(np.append(jjs,jjn),dtype=int)
	ra = np.append(ras,ran)
	dec = np.append(decs,decn)
	
	# Store maximum altitude of tiles
	maxAltit = np.array([_skysub.altit(dec[j],0.,sitelat)[0] for j in range(len(ra))])
	
	iciclo = 0
	ncycle = 2
	xcycle = 0
	ntryes = 400
	tryes = 0
	obs = np.array([np.zeros(len(ii))==0,np.zeros(len(ii))==0,np.zeros(len(ii))==0,np.zeros(len(ii))==0])
		
	MJD_dstart = aux.mjd(2014,01,01) # 01/jan/2014

	exptime = [0.003,0.024]
	
	xx = ii.max()+1
	yy = jj.max()+1
	
	map = np.zeros(xx*yy).reshape(yy,xx)
	for i in range(len(ii)):
		map[jj[i]][ii[i]] = 1.0
	xmap = np.array([map,map,map])

	cmap = colors.ListedColormap(['black', 'gray', 'red','white','white'])
	bounds=[0,1,2,3,4]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	
	#plt.plot(ii,jj,'.')
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1) #[fig.add_subplot(2,2,0),fig.add_subplot(2,2,1),fig.add_subplot(2,2,2),fig.add_subplot(2,2,3)]
	ax = fig.add_axes([0,0,1,1])
	ax.axis("off")

	#for i in range(len(obs)):
	ax.imshow(map,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
	fig.savefig('xmap_%04i.png'%0)

	nmap = 1

	no_obsTray = np.zeros(len(obs)) == 1
	
	fp = open('surveysim_02.dat','w')

	for MJD in np.arange(MJD_dstart,MJD_dstart+365.*2):
		nightStart = _skysub.jd_sun_alt(sunMaxAlt,2400000.5+MJD+1.0, sitelat, sitelong)
		nightEnd   = _skysub.jd_sun_alt(sunMaxAlt,2400000.5+MJD+1.5, sitelat, sitelong)
	
		ramoon = 0.
		decmoon = 0.
		distmoon = 0.
		rasun = 0.
		decsun = 0.
		
		ramoon,decmoon,distmoon = _skysub.lpmoon(nightStart,sitelat,_skysub.lst(nightStart,sitelong))
		
		ill_frac=0.5*(1.-np.cos(_skysub.subtend(ramoon,decmoon,rasun,decsun)))
		
		stdscr.addstr(7, 0, 'Moon illum: %.3f '%(ill_frac))
		stdscr.clrtoeol()
		
		if ill_frac < 0.95:
			iciclo = 0
		else:
			iciclo = -1
		
		stdscr.addstr(0,0,'Observations start at JD = %12.2f'%nightStart)
		stdscr.addstr(1,0,'Observations end at JD   = %12.2f'%nightEnd)
		xnobs=0
		if iciclo >= 0:

			nobs = len(obs[iciclo][obs[iciclo]])

			try:
				obs[iciclo],xnobs,tnobs,emptyObsSlots = make_obs(nightStart,nightEnd,ra,dec,obs[iciclo],exptime[iciclo],maxAltit)
				
				fp.write('%10.2f %6.3f %4i %4i '%(nightStart,nightEnd-nightStart,xnobs,tnobs))
				xnobs = 0
				tnobs = len(emptyObsSlots)
				
				if len(emptyObsSlots) > 0:
					obs[iciclo+1],xnobs,tnobs,emptyObsSlots = make_obs(nightStart,nightEnd,ra,dec,obs[iciclo+1],exptime[iciclo+1],maxAltit)
				fp.write('%4i %4i\n'%(xnobs,tnobs))
				
			except:
				#stdscr.addstr(8,0,sys.exc_info()[0])
				errinfo = traceback.format_exc(sys.exc_info()[2]).split('\n')
				for ierr in range(len(errinfo)):
					stdscr.addstr(11+ierr,0,errinfo[ierr])
				pass

			if nobs == len(obs[iciclo][obs[iciclo]]):
				no_obsTray[iciclo] = True
			else:
				no_obsTray[iciclo] = False


			if no_obsTray.all():
				if  tryes > ntryes:
					break
				else:
					tryes+=1

		else:
			fp.write('%10.2f %6.3f %4i %4i 0 0\n'%(nightStart,nightEnd-nightStart,0.,len(np.arange(nightStart,nightEnd,exptime[iciclo]))))
			stdscr.addstr(7, 20, ' - No observations this night')
		stdscr.addstr(2, 0, ' Observed %i '%(xnobs))
		xjj = jj[np.bitwise_not(obs[iciclo])]
		xii = ii[np.bitwise_not(obs[iciclo])]
		for i in range(len(xii)):
			xmap[iciclo][xjj[i]][xii[i]] = 2.0
		xjj = jj[np.bitwise_not(obs[iciclo+1])]
		xii = ii[np.bitwise_not(obs[iciclo+1])]
		for i in range(len(xii)):
			xmap[iciclo+1][xjj[i]][xii[i]] = 2.0

		xcycle+=1

		#stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
		#stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))

		alldone = np.zeros(ncycle) == 1
		for i in range(ncycle):
			if i == iciclo:
				start = '--> '
			else:
				start = '--- '
			stdscr.addstr(i+3, 0, start+'[Tray: %i] - %4i/%i areas observed'%(i,len(obs[i])-len(obs[i][obs[i]]),len(obs[i])))
			alldone[i] = len(obs[i][obs[i]]) == 0
		stdscr.refresh()

			#print '[Ciclo: %i] - %i/%i areas observed'%(i,len(obs[i])-len(obs[i][obs[i]]),len(obs[i]))
		#for i in range(len(obs)):
		#	ax[i].cla()
		#	ax[i].imshow(xmap[i],aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
		ax.cla()
		ax.imshow(xmap[0]+xmap[1]-1,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
		fig.canvas.draw()
		if not no_obsTray.all():
			fig.savefig('ymap_%04i.png'%nmap)
		nmap += 1
		#plt.plot(ii,jj,'.')
		if alldone.all():
			break

	fp.close()
	print 'Observations started in ',MJD_dstart
	print 'Observations ended in ',MJD
	print 'Survey took %i days'%(MJD-MJD_dstart)
	
	return 0

#
################################################################################

################################################################################
#

if __name__ == '__main__':

	#win = fig.canvas.manager.window
	#fig.canvas.manager.window.after(100, main)
	#plt.show()

	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	
	try:
		main(sys.argv)
	finally:
		curses.echo()
		curses.nocbreak()
		curses.endwin()
