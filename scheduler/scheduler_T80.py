#! /usr/bin/env python

'''
Simulates scheduler operations for T80 South.
'''

import sys
import numpy as np
import _skysub
import matplotlib
matplotlib.use('TkAgg') # do this before importing pylab
import matplotlib.pyplot as plt
from matplotlib import colors
import Image
import curses

sitelat = -30.228
sitelong = 4.715
sunMaxAlt = -18.

def garbage():

		if xcycle == ncycle or nobs == len(obs[iciclo][obs[iciclo]]):
			no_obsTray[iciclo] = True
			stdscr.addstr(2,0,'- Switching tray')
			xcycle = 0
			if iciclo == 3:
				iciclo = 0
			else:
				if nobs != len(obs[iciclo][obs[iciclo]]):
					no_obsTray[iciclo] = False
				iciclo+=1
		else:
			stdscr.addstr(2,0,'')
			stdscr.clrtoeol()
			no_obsTray[iciclo] = False
			tryes = 0


def make_obs(T0,T1,RA,DEC,mask,texp):

	obsmask = np.bitwise_and(np.zeros(len(RA),dtype=int)==0,mask)
	
	i = 0
	
	for time in np.arange(T0,T1,texp):
		
		lst = _skysub.lst(time,sitelong)*360./24.
	
		#lst = _skysub.lst(time,sitelong) #*360./24.
		ha = lst - RA[obsmask]
		alt = np.array([_skysub.altit(DEC[obsmask][i],ha[i],sitelat)[0] for i in range(len(ha))])
		stg = alt.argmax()
	
		#print time,lst,np.sqrt(dist1[stg]),np.sqrt(dist2[stg]),dist[stg],RA[obsmask][stg],DEC[obsmask][stg],stg

		mm = obsmask[obsmask]
		mm[stg] = False
		obsmask[obsmask] = mm
		i+=1
			
	#print i
	return obsmask
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

	iis,jjs,ras,decs,rots = np.loadtxt(opt.south_pt,unpack=True,usecols=(0,1,4,5,6))
	
	iin,jjn,ran,decn,rotn = np.loadtxt(opt.north_pt,unpack=True,usecols=(0,1,4,5,6))
	
	ii = np.array(np.append(iis,iin+iis.max()+10),dtype=int)
	jj = np.array(np.append(jjs,jjn),dtype=int)
	ra = np.append(ras,ran)
	dec = np.append(decs,decn)
	
	iciclo = 0
	ncycle = 3
	xcycle = 0
	ntryes = 400
	tryes = 0
	obs = np.array([np.zeros(len(ii))==0,np.zeros(len(ii))==0,np.zeros(len(ii))==0,np.zeros(len(ii))==0])
		
	MJD_dstart = 56294.5
	exptime = 0.01
	
	xx = ii.max()+1
	yy = jj.max()+1
	
	map = np.zeros(xx*yy).reshape(yy,xx)
	for i in range(len(ii)):
		map[jj[i]][ii[i]] = 1.0
	xmap = np.array([map,map,map])

	cmap = colors.ListedColormap(['black', 'gray', 'red', 'blue', 'blue', 'white'])
	bounds=[0,1,2,3,4,5]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	
	#plt.plot(ii,jj,'.')
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1) #[fig.add_subplot(2,2,0),fig.add_subplot(2,2,1),fig.add_subplot(2,2,2),fig.add_subplot(2,2,3)]
	ax = fig.add_axes([0,0,1,1])
	ax.axis("off")

	#for i in range(len(obs)):
	ax.imshow(map,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
	fig.savefig('map_%04i.png'%0)

	nmap = 1

	no_obsTray = np.zeros(len(obs)) == 1

	for MJD in np.arange(MJD_dstart,MJD_dstart+365.*6):
		nightStart = _skysub.jd_sun_alt(sunMaxAlt, MJD, sitelat, sitelong)
		nightEnd   = _skysub.jd_sun_alt(sunMaxAlt, MJD+0.5, sitelat, sitelong)
	
	
		ramoon = 0.
		decmoon = 0.
		distmoon = 0.
		rasun = 0.
		decsun = 0.
		
		ramoon,decmoon,distmoon = _skysub.lpmoon(nightStart,sitelat,_skysub.lst(nightStart,sitelong))
		
		ill_frac=0.5*(1.-np.cos(_skysub.subtend(ramoon,decmoon,rasun,decsun)))
		
		stdscr.addstr(7, 0, 'Moon illum: %.3f '%(ill_frac))
		stdscr.clrtoeol()
		
		if ill_frac < 0.25:
			iciclo = 0
		elif ill_frac < 0.75:
			iciclo = 1
		elif ill_frac < 0.95:
			iciclo = 2
		else:
			iciclo = -1
		
		stdscr.addstr(0,0,'Observations start at JD = %12.2f'%nightStart)
		stdscr.addstr(1,0,'Observations end at JD   = %12.2f'%nightEnd)

		if iciclo >= 0:

			nobs = len(obs[iciclo][obs[iciclo]])
		
			if len(obs[iciclo][obs[iciclo]]) > 1:
				try:
					obs[iciclo] = make_obs(nightStart,nightEnd,ra,dec,obs[iciclo],exptime)
				except:
					pass
			elif (len(obs[0][obs[0]]) == 0 and len(obs[1][obs[1]]) == 0 and len(obs[2][obs[2]]) == 0 and len(obs[3][obs[3]]) == 0):
				break

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
			stdscr.addstr(7, 20, ' - No observations this night')

		xjj = jj[np.bitwise_not(obs[iciclo])]
		xii = ii[np.bitwise_not(obs[iciclo])]
		for i in range(len(xii)):
			xmap[iciclo][xjj[i]][xii[i]] = 2.0

		xcycle+=1

		#stdscr.addstr(0, 0, "Moving file: {0}".format(filename))
		#stdscr.addstr(1, 0, "Total progress: [{1:10}] {0}%".format(progress * 10, "#" * progress))

		for i in range(ncycle):
			if i == iciclo:
				start = '--> '
			else:
				start = '--- '
			stdscr.addstr(i+3, 0, start+'[Tray: %i] - %4i/%i areas observed'%(i,len(obs[i])-len(obs[i][obs[i]]),len(obs[i])))
		stdscr.refresh()
			#print '[Ciclo: %i] - %i/%i areas observed'%(i,len(obs[i])-len(obs[i][obs[i]]),len(obs[i]))

		#for i in range(len(obs)):
		#	ax[i].cla()
		#	ax[i].imshow(xmap[i],aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
		ax.cla()
		ax.imshow(xmap[0]+xmap[1]+xmap[2]-2,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
		fig.canvas.draw()
		if not no_obsTray.all():
			fig.savefig('map_%04i.png'%nmap)
		nmap += 1
		#plt.plot(ii,jj,'.')

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
