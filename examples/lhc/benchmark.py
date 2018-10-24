#!/usr/bin/env python3

import time, sys

import numpy as np

import sixtracktools
import simpletrack as sim


def speed(cljob,npart=20000,turns=10,device="0.0"):
  particles = sim.Particles(nparticles=npart)
  particles.p0c=7000e6
  particles.px=np.linspace(0,0.0000,npart)
  cljob.set_particles(particles)
  start=time.time()
  cljob.track(10)
  cljob.collect()
  duration=(time.time()-start)
  return duration/turns, duration/(npart*turns)

if len(sys.argv)>1:
    device=sys.argv[1]
else:
    device="0.0"

if len(sys.argv)>2:
    start=int(sys.argv[2])
else:
    start=1

if len(sys.argv)>3:
    step=int(sys.argv[3])
else:
    step='log10'

if len(sys.argv)>4:
    stop=int(sys.argv[4])
    fact=100
else:
    stop='long'
    fact=3

elements=sim.Elements()

six = sixtracktools.SixInput('.')
line, rest, iconv = six.expand_struct(convert=elements.gen_builder())

particles = sim.Particles(nparticles=1)
particles.p0c=7000e6
cljob = sim.TrackJobCL(particles, elements, device=device,dump_element=0)

print(f"turns npart t/turn[ms] t/turn/part[us]")
turns=10
sp1,rsp1=speed(cljob,1,turns,device=device)
sp=0; npart=start;
while sp<fact*sp1:
    sp,rsp=speed(cljob,npart,turns,device=device)
    print(f"{turns:5} {npart:5} {sp*1e3:4.2f} {rsp*1e6:8.2f}")
    if step=='log10':
       npart+=10**int(np.log10(npart))
    else:
       npart+=step
    if not stop=='long':
       if npart>stop:
          break

