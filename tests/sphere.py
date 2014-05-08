import pylab as py
import matplotlib.figure
import matplotlib.backends.backend_agg
import numpy
from numpy import pi

img = numpy.random.random((800, 800))
fig = matplotlib.figure.Figure((10, 4.9))
ax = fig.add_subplot(1,1,1,projection='mollweide')
image = ax.imshow(img, extent=(-pi,pi,-pi/2,pi/2), clip_on=False, aspect=0.5)
cb = fig.colorbar(image, orientation='horizontal')
canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
canvas.print_figure("hi.png")
