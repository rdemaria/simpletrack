import time

import numpy as np

import sixtracktools
import simpletrack as sim

elements=sim.Elements()

six = sixtracktools.SixInput('.')
line, rest, iconv = six.expand_struct(convert=elements.gen_builder())

def speed(npart=20000,turns=10):
  particles = sim.Particles(nparticles=npart)
  particles.p0c=7000e6
  particles.px=np.linspace(0,0.0000,npart)
  cljob = sim.TrackJobCL(particles, elements, device="0.0",dump_element=0)
  start=time.time()
  cljob.track(10)
  cljob.collect()
  duration=(time.time()-start)
  return duration/turns, duration/(npart*turns)


print(f"turns npart t/turn[ms] t/turn/part[us]")
for turns in [10]:
  for npart in (1,1000,5000,10000,20000,30000,40000):
    sp,rsp=speed(npart,turns)
    print(f"{turns:5} {npart:5} {sp*1e3:4.2f} {rsp*1e6:8.2f}")


