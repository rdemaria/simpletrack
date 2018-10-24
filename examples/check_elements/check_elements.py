import sys

import numpy as np

import pysixtrack as six
import simpletrack as sim

def check_diff(name,p,pref,tol,rtol):
    v=getattr(p,name)[0]
    vref=getattr(p,name)[0]
    diff=vref-v
    if abs(vref)>0:
        rdiff=diff/vref
    else:
        rdiff=0
    if abs(diff)>tol or abs(rdiff)>rtol or np.isnan(diff):
        print(f"{name:5}: {v:17.12g} {vref:17.12g} {diff:17.12g} {rdiff:17.12g}")
    return diff,rdiff

def mktest(epdata,tol,rtol,elem,**elemdata):
     pref= six.Particles(**pdata)
     p = sim.Particles(nparticles=1)
     for k,v in pdata.items():
        setattr(p,k,v)
     getattr(six,elem)(**elemdata).track(pref)
     elements = sim.Elements()
     getattr(elements,elem)(**elemdata)
     cljob = sim.TrackJobCL(p, elements, device="0.0")
     cljob.track(1)
     cljob.collect()
     tdiff=0
     trdiff=0
     print(elem,elemdata)
     for coord in 'x px y py zeta delta rvv rpp beta0'.split():
         diff,rdiff=check_diff(coord,p,pref,tol,rtol)
         tdiff+=diff**2
         trdiff+=rdiff**2
     if np.sqrt(tdiff)>tol or np.sqrt(tdiff)>rtol:
         print(f"Sum  : {tdiff:17.12g} {rdiff:17.12g}")
         return False
     else:
         return True

tol=-1

pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,delta=1)
#Drift
mktest(pdata,tol,0,'Drift',length=1.0)

#Multipole
pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,x=1e-3,y=2e-3,delta=1)
mktest(pdata,tol,0,'Multipole',knl=[1.])
mktest(pdata,tol,0,'Multipole',ksl=[1.])
mktest(pdata,tol,0,'Multipole',knl=[3.],ksl=[2.])
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.])
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3)
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3,hyl=1e-3)
mktest(pdata,tol,0,'Multipole',knl=[1.])
mktest(pdata,tol,0,'Multipole',ksl=[1.])
mktest(pdata,tol,0,'Multipole',knl=[3.],ksl=[2.])
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.])
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3)
mktest(pdata,tol,0,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3,hyl=1e-3)

#XYShift
mktest(pdata,tol,0,'XYShift',dx=1,dy=2)
mktest(pdata,tol,0,'SRotation',angle=60)

#pdata=dict(mass0=3,p0c=4,zeta=0.01)
##Drift
#mktest(pdata,tol,0,'Cavity',voltage=3.544004,lag=90)

