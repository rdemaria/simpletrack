#!/usr/bin/env python3

import time, sys

import numpy as np

import sixtracktools
import simpletrack as sim

elements=sim.Elements()

six = sixtracktools.SixInput('.')
line, rest, iconv = six.expand_struct(convert=elements.gen_builder())

def speed(npart=20000,turns=10,device="0.0"):
  particles = sim.Particles(nparticles=npart)
  particles.p0c=7000e6
  particles.px=np.linspace(0,0.0000,npart)
  cljob = sim.TrackJobCL(particles, elements, device=device,dump_element=0)
  start=time.time()
  cljob.track(10)
  cljob.collect()
  duration=(time.time()-start)
  return duration/turns, duration/(npart*turns)

if len(sys.argv)==2:
    device=sys.argv[1]
else:
    device="0.0"

print(f"turns npart t/turn[ms] t/turn/part[us]")
turns=10
sp1,rsp1=speed(1,turns,device=device)
sp=0; npart=4;
while sp<3*sp1:
    sp,rsp=speed(npart,turns,device=device)
    print(f"{turns:5} {npart:5} {sp*1e3:4.2f} {rsp*1e6:8.2f}")
    npart=int(npart*np.sqrt(2))

