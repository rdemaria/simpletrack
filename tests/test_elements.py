import sys

import numpy as np

import pysixtrack as six
import simpletrack as sim

def check_diff(name,p,pref,tol,rtol):
    v=getattr(p,name)[0]
    vref=getattr(pref,name)
    diff=vref-v
    if abs(vref)>0:
        rdiff=diff/vref
    else:
        rdiff=0
    if abs(diff)>tol or abs(rdiff)>rtol or np.isnan(diff):
        print(f"{name:5}: {v:17.12g} {vref:17.12g} {diff:17.12g} {rdiff:17.12g}")
    return diff,rdiff

def mktest(pdata,tol,rtol,elem,**elemdata):
     pref= six.Particles(**pdata)
     p = sim.Particles(nparticles=1)
     for k,v in pdata.items():
        setattr(p,k,v)
     getattr(six,elem)(**elemdata).track(pref)
     elements = sim.Elements()
     getattr(elements,elem)(**elemdata)
     cljob = sim.TrackJobCL(p, elements, device="0.0", debug=False)
     cljob.track(1)
     cljob.collect()
     tdiff=0
     trdiff=0
     print(elem,elemdata)
     for coord in 'x px y py zeta delta rvv rpp beta0'.split():
         diff,rdiff=check_diff(coord,p,pref,tol,rtol)
         tdiff+=diff**2
         trdiff+=rdiff**2
     tdiff=np.sqrt(tdiff)
     trdiff=np.sqrt(trdiff)
     if tdiff>tol or trdiff>rtol:
         print(f"Sum  : {tdiff:17.12g} {trdiff:17.12g}")
         return False
     else:
         return True

def test_drift():
  pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,delta=1)
  assert mktest(pdata,3e-16,2e-16,'Drift',length=0.0)
  assert mktest(pdata,4e-16,2e-16,'Drift',length=0.0)

def test_multipole():
    pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,x=1e-3,y=2e-3,delta=0)
    assert mktest(pdata,0,0,'Multipole',knl=[1.])
    assert mktest(pdata,0,0,'Multipole',ksl=[1.])
    assert mktest(pdata,0,0,'Multipole',knl=[3.],ksl=[2.])
    pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,x=1e-3,y=2e-3,delta=1)
    assert mktest(pdata,3e-16,2e-16,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3)
    assert mktest(pdata,3e-16,2e-16,'Multipole',knl=[0,3.],ksl=[2.],length=1.0,hxl=1e-3,hyl=1e-3)

#
##Align
def test_align():
    pdata=dict(mass0=3,p0c=4,px=1e-3,py=2e-3,x=1e-3,y=2e-3,delta=0)
    assert mktest(pdata,0,0,'XYShift',dx=1,dy=2)
    assert mktest(pdata,0,0,'SRotation',angle=60)

def test_cavity():
    pdata=dict(mass0=3,p0c=4,zeta=0.01)
    assert mktest(pdata,6e-16,6e-16,'Cavity',voltage=3.544004,lag=90)

