import sys,os
import pyopencl as cl
import pyfits
import numpy
import time

class CL:

	path = '/Volumes/TiagoHD2/data/Grade5results'
	ifile = 'CCD0_Mode0_1x1_5Ke-CTE.fits'
	
	window = [100,100]

	ofile = 'windowed.fits'

	def __init__(self):
		self.ctx = cl.create_some_context()
		self.queue = cl.CommandQueue(self.ctx)

	def loadProgram(self, filename):
		#read in the OpenCL source file as a string
		f = open(filename, 'r')
		fstr = "".join(f.readlines())
		print fstr
		#create the program
		self.program = cl.Program(self.ctx, fstr).build()

	def popCorn(self):
		mf = cl.mem_flags

		#initialize client side (CPU) arrays
		#self.a = numpy.array(range(10), dtype=numpy.float32)
		#self.b = numpy.array(range(10), dtype=numpy.float32)
		self.data = pyfits.getdata(os.path.join(self.path,self.file1))

		#create OpenCL buffers
		#self.imagebuf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=self.ra1)
		
		self.imagebuf = cl.image_from_array(self.ctx,self.data)
		
		self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.dec2.nbytes)

	def execute(self):

		match1 = numpy.array([],dtype=int)
		match2 = numpy.array([],dtype=int)
		
		nmatch1 = numpy.array([],dtype=int)
		nmatch2 = numpy.array([],dtype=int)
		#i = 0
		for i in range(len(self.ra1)):
		
		
			val1 = numpy.float32(self.ra1[i])
			val2 = numpy.float32(self.dec1[i])
			#len1 = numpy.uint16(len(self.ra1))
			#len2 = numpy.uint16(len(self.ra2))
			
			
			self.program.angdist(self.queue,
								self.dec2.shape,
								None,
								val1,
								val2,
								self.ra2_buf,
								self.de2_buf,
								self.dest_buf)
			c = numpy.empty_like(self.dec2)
			cl.enqueue_read_buffer(self.queue, self.dest_buf, c).wait()

			m = c.argmin()
			if c[m] * 60. * 60. < ( numpy.sqrt(self.yerr[i]**2 + self.xerr[i]**2) * self.scale ) * 3.:

				match1 = numpy.append(match1,i)
				match2 = numpy.append(match2,m)
				
			else:
				nmatch1 = numpy.append(nmatch1,i)
				nmatch2 = numpy.append(nmatch2,m)

			if i % 1000 == 0:
				sys.stdout.write('\r# [%6i/%6i] - Found %6i M | %6i NM' % (i,len(self.ra1),len(match1),len(nmatch1)) )
				sys.stdout.flush()
		numpy.save(self.ofile,arr=(match1,match2))
		numpy.save('n'+self.ofile,arr=(nmatch1,nmatch2))
		print ''
		print '# - Found %i/%i matches'%(len(match1),len(self.ra1))
		print '# - Found %i/%i no matches'%(len(nmatch1),len(self.ra1))
		#print "a", self.a
		#print "b", self.b
		#print "c", c



if __name__ == "__main__":
	example = CL()
	example.loadProgram("angdist.cl")
	example.popCorn()
	print time.strftime('%D %H:%M:%S')
	example.execute()
	print time.strftime('%D %H:%M:%S')
