import h5py
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm

fileIn = "../statistics"
#time = np.genfromtxt(fileIn, usecols=(1,), comments="#", dtype=None, encoding='ascii')
time = np.genfromtxt(fileIn, usecols=(1,), comments="#", dtype=None)

Files = np.genfromtxt(fileIn, usecols=(24,), comments="#", dtype=None)

#print Files
filefilter = Files != '""'
#print Files[filefilter]

times2 = time[filefilter] / (1e6)
#print times2

particles = sorted(glob.glob("particles*h5"))

P2 = np.array([])
T2 = np.array([])
times3 = np.array([])

id = 3519
j=0
for p in particles:
	
	# mesh-02165.h5 mesh-02588.h5
	part = h5py.File(p,'r')
	#particles.keys()
	#[u'T', u'id', u'initial lower', u'initial mantle', u'initial position', u'initial seed', u'initial upper', u'nodes', u'p']
	lower = part['initial lower'][:]
	idx = part['id']
	#print idx[lower[:,0] > 0.5]
	P = part['p']
	#P1 = P[idx == id][0]
	P1 = np.mean(P[:][0]) / 1e9
	T = part['T']
	#T1 = T[idx == id][0] - 273.0
	T1 = np.mean(T[:][0]) - 273.0
	print "PT:", times2[j],P1, T1
	T2 = np.append(T2,T1)
	P2 = np.append(P2,P1)
	times3 = np.append(times3,times2[j])
	j+=1

np.savetxt("PT.dat", np.c_[times3,P2, T2], fmt='%.4f %.4f %.4f', header="Times	P  T")

ax = plt.subplot(1,1,1)
#file2 = str2+'_Mob.png'
#plt.plot(T2,P2,color='red', alpha=1.00)
#colors = plt.cm.jet(np.linspace(0,1,len(times3)))
cmap = mpl.cm.cool
norm = mpl.colors.Normalize(vmin=np.min(times3), vmax=np.max(times3))
sc= plt.scatter(T2,P2,c=times3,cmap='cool',s=times3)
plt.plot(T2,P2,'b-',alpha=0.2,linewidth=3)
ax.invert_yaxis()
plt.colorbar(sc)
plt.show()



#plt.savefig(file2)


