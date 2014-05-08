import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
from matplotlib.collections import PatchCollection

fig = plt.figure()
ax = fig.add_subplot(111,projection='mollweide')


pt = np.loadtxt('coordinatesystemandtiling/norpointT80.dat',unpack=True)

myPatches=[]

for i in range(len(pt[0])):
    r2 = patches.RegularPolygon((pt[4][i]*np.pi/180.,pt[5][i]*np.pi/180.),4,0.573*np.pi/180.*np.pi,orientation=(45-pt[6][i])*np.pi/180.)
	#t2 = mpl.transforms.Affine2D().rotate_deg(pt[6][i]) #+ ax.transData
    #r2.set_transform(t2)
    myPatches.append(r2)


plt.grid(True)
#plt.xlim(0,360)
#plt.ylim(-90,90)

#plt.xlim(-80,80)
#plt.ylim(-80,80)


collection = PatchCollection(myPatches,alpha=0.5)
ax.add_collection(collection)

plt.show()