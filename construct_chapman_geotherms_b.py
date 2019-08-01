import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm

#UHT = 1500C/GPa
# 1 GPa ~ 33km
# dT/dz ~ 0.044, k=3
# Q ~ 0.132 ~ 132 mW/m3


# Initial temperature field
# Typical continental geotherm based on equations 4-6 from:
#   D.S. Chapman (1986), "Thermal gradients in the continental crust",
#   Geological Society of London Special Publications, v.24, p.63-70.
# The initial constraints are:
#   Layer Surface Temperature - upper crust (ts1) = 273 K; 
#                               mantle      (ts3) = 823 K;  
#   Model Base Temperature - (tb) = 1573 K;
#   Heat Production - upper crust (A) = 1.5e-6 W/m^3; 
#   Thermal Conductivity - upper crust (k1) = 2.5 (W/(m K)); 
#                          lower crust (k2) = 2.5 (W/(m K)); 
#                          mantle      (k3) = 3.3 (W/(m K));
# To satisfy these constraints, the following values are required:
#   Layer Surface Heat Flow - upper crust (qs1) = 0.065357 W/m^2; 
#                             lower crust (qs2) = 0.035357 W/m^2; 
#                             mantle      (qs3) = 0.035357 W/m^2;
#   Temperature - base of upper crust (ts2) = 681.5714

y = np.linspace(0,100e3,101)

d1 = 10.e3
d2=20.e3
d3=100.e3

k1=2.9
k2=3.3
k3=3.8
A1=10.e-6  #10 for granites current, ~3 for metaseds
A2=0.9e-6   # From Chapman lower crust best estimate, x2 for Proterozoic
A3=0.
h=100e3
ts1=288

colors = "bgrcmykw"
color_index = 0

#for qs1 in np.array([130,140,150,160,170]):
for qs1 in np.arange(120,170,10):
    #qs1=0.1353571
    qs1 /= 1e3
    qs2 = qs1 - A1*d1
    ts2 = ts1 + qs1*d1/k1 -( A1*d1**2)/(2*k1)

    #ts2=781.5714   #Derivative

    qs3 = qs2 - A2*(d2-d1)
    ts3 = ts2 + qs2*(d2-d1)/k2 -( A2*(d2-d1)**2)/(2*k2)
    ts4 = ts3 + qs3*(d3-d2)/k3 - ( A3*(d3-d2)**2)/(2*k3)

    print "Temps",ts2,ts3,ts4
    print "Q    ",qs1,qs2,qs3
    T = np.zeros_like(y)

    for i in np.arange(len(y)):
        if(y[i])<=d1:
          T[i] = ts1 + (qs1/k1)*(y[i]) - (A1*(y[i])*(y[i]))/(2.0*k1)
          #print i, T[i]

        elif((y[i])>d1 and (y[i]))<=d2:
          T[i] = ts2 + (qs2/k2)*(y[i]-d1) - (A2*(y[i]-d1)*(y[i]-d1))/(2.0*k2)
        else:
          #T = ts3 + (qs3/k3)*(h-y-d2);
          T[i] = ts3 + (qs3/k3)*(y[i]-d2) - (A3*(y[i]-d2)*(y[i]-d2))/(2.0*k3)

    #print np.c_[h-y,T]

    plt.plot(T-273,y,c=colors[color_index])
    plt.annotate(qs1*1e3,xytext=(np.max(T-273)-200,100e3),xy=(np.max(T-273),1e5),color=colors[color_index])
    color_index += 1

plt.xlabel("Temperature (C)")
plt.ylabel("Depth (km)")
#plt.xlim(0,np.max(T))
plt.gca().invert_yaxis()
plt.gca().set_ylim(top=0)
plt.gca().set_xlim(left=0)
plt.tight_layout()
plt.savefig('Initial_geotherms_b.png')
plt.show()



