#! /usr/bin/env python

'''
Simulates scheduler operations for T80 South.
'''

import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import _skysub
from surveysimF import *
import auxiliar as aux
import curses

################################################################################
#

def main(argv):

	'''
	Main function. Reads input parameters, run scheduler and stores results.
	'''

	from optparse import OptionParser
	
	parser = OptionParser()

	parser.add_option("-m",'--meteorology',
                      help='''
Input file. This file contains weather information. Only clouded nights need be 
specified. Format is MJD FLAG, where FLAG is 
0 - Good night. Less than 0.5 mag extinction (may be skipped)
1 - Thin Cirrus. Between 0.5 and 2 mag extinction.
2 - Cloudy. Between 2 and 4 mag extinction.
3 - Closed.'''
					  ,type="string")
	parser.add_option("-s", '--savefig',action="store_true", default=False,
                      help="Save images of survey evolution.")
	parser.add_option("-v", '--verbose',action="store_true", dest="verbose", default=False,
                      help="Don't print status messages to stdout")
    
	opt,arg = parser.parse_args(argv)
			
	#
	# Reading input files
	#

	_path = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/')

	sna_file = os.path.join(_path,'smaps_pointT80norte.dat')
	ssa_file = os.path.join(_path,'smaps_pointsulT80.dat')

	#var_file = os.path.join(_path,'../splus_varregions.dat')
	var_file = os.path.join(_path,'des_sna.dat')
	
	#
	# North and south galactic regions
	#
	iis,jjs,ras,decs,rots = np.loadtxt(sna_file,unpack=True,usecols=(0,1,4,5,6))
	
	iin,jjn,ran,decn,rotn = np.loadtxt(ssa_file,unpack=True,usecols=(0,1,4,5,6))

	ii = np.array(np.append(iis,iin+iis.max()+10),dtype=int)
	jj = np.array(np.append(jjs,jjn),dtype=int)
	ra = np.append(ras,ran)
	dec = np.append(decs,decn)

	#
	# Variability regions
	#
	iiv,jjv,rav,decv,rotv = np.loadtxt(var_file,unpack=True,usecols=(0,1,4,5,6))
		
	#ObsSim = SurveySim([ra],[dec],[ii],[jj],1,[0.05])
	ObsSim = SurveySim([ra,rav],[dec,decv],[ii,iiv],[jj,jjv],2,[0.05,0.05])
	ObsSim.setupSPLUS(1,-1,7)
	#ObsSim.setupSPLUS(0,10,7,0.05)
	sinfo = 'surveysim_05.txt'
	storeImage='amap_%04i.png'
	#ObsSim = SurveySim(ra,dec,ii,jj,1,[0.03])
	
	MJD_dstart = aux.mjd(2014,01,01) # 01/jan/2014

	exptime = [0.003,0.024]
	
	MJD = MJD_dstart
	SurveyLength = 365.*2 # two years top
	#for MJD in np.arange(MJD_dstart,MJD_dstart+365.*2):
	
	cmap = colors.ListedColormap(['black', 'gray', 'green', 'red', 'blue', 'white'])
	bounds=[0,1,2,3,4,5]
	norm = colors.BoundaryNorm(bounds, cmap.N)

	fig = plt.figure()
	ax1 = fig.add_axes([0,0,1,1])
	ax1.axis("off")
	#ax2 = fig.add_axes([0,0,1,0.5])
	#ax2.axis("off")

	nmap = 0
	fp = open(sinfo,'w')
	#while ( (not ObsSim.allDone()) and (MJD < MJD_dstart+SurveyLength) ) :
	totalTiles = ObsSim.Tiles()*ObsSim.ntrays
	
	while ( ObsSim.obsTiles(0) > 0 ) :
			
		nightStart = _skysub.jd_sun_alt(ObsSim.sunMaxAlt,2400000.5+MJD+1.0, ObsSim.sitelat, ObsSim.sitelong)
		nightEnd   = _skysub.jd_sun_alt(ObsSim.sunMaxAlt,2400000.5+MJD+1.5, ObsSim.sitelat, ObsSim.sitelong)
		'''
		ramoon = 0.
		decmoon = 0.
		distmoon = 0.
		rasun = 0.
		decsun = 0.
		
		ramoon,decmoon,distmoon = _skysub.lpmoon(nightStart,ObsSim.sitelat,_skysub.lst(nightStart,ObsSim.sitelong))
		
		ill_frac=0.5*(1.-np.cos(_skysub.subtend(ramoon,decmoon,rasun,decsun)))
		
		if ill_frac < 0.95:
		'''
		#print 'Running...'
		info,queue,queueInfo = ObsSim.makeObs(nightStart,nightEnd)

		for jj,ii in enumerate(info):
			if jj < 20:
				stdscr.addstr(jj,0,'[%2i] - %s'%(jj,ii))
			else:	
				break
		stdscr.refresh()

		fp.write(queueInfo+'\n')

		if opt.savefig:
			map1 = ObsSim.trayImage(0)
			#map2 = ObsSim.trayImage(1)
			
			ax1.cla()
			ax1.imshow(map1,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
			ax1.annotate(	'Day: %5.0f\nTiles: %5i/%5i'%(MJD-MJD_dstart+1,ObsSim.obsTiles(0),ObsSim.nTiles(0)),
							rotation=0, xy=(.5, .9),  xycoords='axes fraction',
							horizontalalignment='center', verticalalignment='center',
							color='w')
			'''
			ax2.cla()
			ax2.imshow(map2,aspect='auto',interpolation='nearest',cmap=cmap, norm=norm)
			ax2.annotate(	'Day: %5.0f\nTiles: %5i/%5i'%(MJD-MJD_dstart+1,ObsSim.obsTiles(1),ObsSim.nTiles(1)),
							rotation=0, xy=(.5, .9),  xycoords='axes fraction',
							horizontalalignment='center', verticalalignment='center',
							color='w')
			'''
			fig.canvas.draw()
			#plt.show()
			#return 0
			fig.savefig(storeImage%nmap)
			nmap += 1
			
		MJD+=1.0
	#	for ii in queue:
	#		print ii

	fp.close()

	fp = open('nvisits','w')
	
	for i in range(len(ObsSim.repeatInfo['nobs'])):
		fp.write('%i %i\n'%(ObsSim.repeatInfo['tile'][i],ObsSim.repeatInfo['nobs'][i]))

	fp.close()

	return 0

#
################################################################################

################################################################################
#

if __name__ == '__main__':

	#win = fig.canvas.manager.window
	#fig.canvas.manager.window.after(100, main)
	#plt.show()
	#main(sys.argv)

	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	
	try:
		main(sys.argv)
	finally:
		curses.echo()
		curses.nocbreak()
		curses.endwin()
