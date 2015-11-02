#!/usr/bin/env python

################################################################################

import sys, os
import time
import numpy as np
from astropy.table import Table

import datetime as dt

from chimera.core.cli import ChimeraCLI,action

#from chimera.core.site import datetimeFromJD

################################################################################

class Date2JD (ChimeraCLI):

	############################################################################
	
	def __init__(self):
		ChimeraCLI.__init__(self, "date2JD",
							"Convert date to JD", 0.0, port=9010)

		self.addController(name="site",
				   cls="Site",
				   required=True,
				   help="Observing site",
				   helpGroup="OBSERVATORY")

		self.addParameters(dict(name="filename", long="file", short="f",
								default="",
								help="Filename with parameters for scheduling algorith.",
								metavar="FILENAME"))

		self.addParameters(dict(name="output", long="output", short="o",
								default="",
								help="Output file name.",
								metavar="OUTPUT"))

	############################################################################

	@action(long="date2jd",
		help="Run procedure.",
		actionGroup="")
	def date2jd(self,opt):

		data = Table.read(opt.filename,format='ascii.no_header')
		site = self.site
		
		output = np.zeros(len(data))
		
		for ii,dd in enumerate(data['col1']):
			yyyymmaa,hhmmss = dd.split('T')
			yyyy,mm,aa = [int(val) for val in yyyymmaa.split('-')]
			hh,MM,ss = [int (val) for val in hhmmss.split(':')]
			obs_dt = dt.datetime(yyyy,mm,aa,hh,MM,ss)
			output[ii] = site.JD(obs_dt)

		np.savetxt(opt.output,X=zip(output),fmt='%.6f')

################################################################################

def main(argv):
	
	cli = Date2JD()
	cli.run(argv)
	cli.wait()

################################################################################

if __name__ == '__main__':
	
	main(sys.argv)

################################################################################