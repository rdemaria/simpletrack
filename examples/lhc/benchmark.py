#!/usr/bin/env python3

import time, sys

import numpy as np

import sixtracktools
import pysixtrack
import simpletrack as sim



def speed(cljob,npart=20000,turns=10,trials=1):
  particles = sim.Particles(nparticles=npart)
  particles.p0c=7000e9
  particles.px=np.linspace(0,0.000001,npart)
  cljob.set_particles(particles)
  avg=0
  for i in range(trials):
      start=time.time()
      cljob.track(turns)
      cljob.collect()
      duration=(time.time()-start)
      avg+=duration
  duration=avg/trials
  return duration/turns, duration/(npart*turns)


if len(sys.argv)>1:
    device=sys.argv[1]
else:
    device="0.0"

if len(sys.argv)>2:
    turns=int(sys.argv[2])
else:
    turns=10

if len(sys.argv)>3:
    start=int(sys.argv[3])
else:
    start=1

if len(sys.argv)>4:
    step=int(sys.argv[4])
else:
    step='log10'

if len(sys.argv)>5:
    stop=int(sys.argv[5])
    fact=10000
else:
    stop='long'
    fact=3

elements=sim.Elements()

six = sixtracktools.SixInput(".")
line, other = pysixtrack.Line.from_sixinput(six,classes=elements.gen_builder_class())
iconv = other["iconv"]


particles = sim.Particles(nparticles=1)
particles.p0c=7000e6
cljob = sim.TrackJobCL(particles, elements, device=device,dump_element=0)
cljob.print_devices()

print(f"turns    npart t/turn[ms] t/turn/part[us]")
sp1,rsp1=speed(cljob,1,turns)
sp=0; npart=start;
while sp<fact*sp1:
    sp,rsp=speed(cljob,npart,turns,trials=1)
    print(f"{turns:5} {npart:8} {sp*1e3:10.2f} {rsp*1e6:10.2f}")
    if step=='log10':
       npart+=10**int(np.log10(npart))
    else:
       npart+=step
    if not stop=='long':
       if npart>stop:
          break

