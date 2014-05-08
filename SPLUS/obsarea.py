#! /usr/bin/env python

import sys,os
import numpy as np
import pylab as py
from matplotlib import colors
import _skysub
import auxiliar as aux

################################################################################

sitelat = -30.228
sitelong = 4.715
sunMaxAlt = -18.

################################################################################

def main(argv):
	'''
	Calculates observable area per month.
	'''
	
	_path = os.path.expanduser('~/Develop/SMAPs/coordinatesystemandtiling/')

	sna_file = os.path.join(_path,'smaps_pointT80norte.dat')
	ssa_file = os.path.join(_path,'smaps_pointsulT80.dat')

	iis,jjs,ras,decs,rots = np.loadtxt(sna_file,unpack=True,usecols=(0,1,4,5,6))
	
	iin,jjn,ran,decn,rotn = np.loadtxt(ssa_file,unpack=True,usecols=(0,1,4,5,6))
	
	print 'Total number of tiles: %i'%(len(iis)+len(iin))
	print 'South region tiles: %i'%len(iis)
	print 'North region tiles: %i'%len(iin)
			
	ii = np.array(np.append(iis,iin+iis.max()+10),dtype=int)
	jj = np.array(np.append(jjs,jjn),dtype=int)
	ra = np.append(ras,ran)
	dec = np.append(decs,decn)

	xx = ii.max()+10
	yy = jj.max()+10

	ii+=5
	jj+=5

	fig = py.figure(1)#,figsize=(10,4))
	#ax = fig.add_axes([0.05,0.,0.90,1])
	#ax.axis("off")

	map = np.zeros(xx*yy).reshape(yy,xx)
	for i in range(len(ii)):
		map[jj[i]][ii[i]] = 1.0

	cmap = colors.ListedColormap(['black', 'gray', 'red', 'blue', 'blue', 'white'])
	bounds=[0,1,2,3,4,5]
	norm = colors.BoundaryNorm(bounds, cmap.N)

	month = np.arange(12)
	ndays = [31,28,31,30,31,30,31,31,30,31,30,31]
	nmonth = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct','Nov','Dec']
	imm = 1
	for mm in month:
		dateStart = aux.mjd(2014,mm+1,01)
		dateEnd = aux.mjd(2014,mm+1,ndays[mm])

		obshours = 0.

		for date in np.linspace(dateStart,dateEnd,ndays[mm]):
			nightStart = _skysub.jd_sun_alt(sunMaxAlt, 2400000.5+date+1.0, sitelat, sitelong)
			nightEnd   = _skysub.jd_sun_alt(sunMaxAlt, 2400000.5+date+1.5, sitelat, sitelong)
			#print 'Night start: ',nightStart
			#print 'Night end: ',nightEnd
			#print 'Duration: %f (hours)'%((nightEnd-nightStart)*24.0)
			obshours+=(nightEnd-nightStart)*24.0
			lst_start = _skysub.lst(nightStart,sitelong)#*360./24.
			lst_end = _skysub.lst(nightEnd,sitelong)#*360./24.
			#ha = lst - RA[obsmask]

			#print 'LST @ Start: %f'%(lst_start)
			#print 'LST @ end:   %f'%(lst_end)
			obsmask = np.zeros_like(map) == 0
			
			if lst_start < lst_end:
				obsmask = np.bitwise_and(ra > lst_start*360./24., ra < lst_end*360./24.)
			else:
				obsmask1 = ra > lst_start*360./24.
				obsmask2 = np.bitwise_and(ra > 0.,ra < lst_end*360./24.)
				obsmask = np.bitwise_or(obsmask1,obsmask2)
			for i in np.arange(len(ii))[obsmask]:
				map[jj[i]][ii[i]] = 2
				
		print '%s & %3i & %7.3f & %7.2f \\ \\'%(nmonth[mm],len(map[map>1]),obshours/ndays[mm],obshours)

		ax = fig.add_subplot(4,3,imm)
		ax.cla()
		ax.axis("off")
		dmap = np.array(map)
		ax.imshow(dmap,interpolation='nearest',cmap=cmap, norm=norm)
		ax.set_title(nmonth[imm-1])
		#py.show()
		fig.canvas.draw()
		#fig.savefig('xmap_%02i.png'%(mm+1))
		mask = map > 0
		map[mask] = 1.0
		imm+=1
		#py.show()

	fig.subplots_adjust(wspace=0.01,hspace=0)
	py.show()

	return 0

################################################################################

if __name__ == '__main__':

	main(sys.argv)