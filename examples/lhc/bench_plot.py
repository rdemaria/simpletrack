#!/usr/bin/env python3

import time, sys

import numpy as np

import simpletrack as sim


def speed(cljob,npart=20000,turns=10):
  particles = sim.Particles(nparticles=npart)
  particles.p0c=7000e9
  particles.px=np.linspace(0,0.000001,npart)
  cljob.set_particles(particles)
  start=time.time()
  cljob.track(turns)
  cljob.collect()
  duration=(time.time()-start)
  return duration

elements=sim.Elements.fromfile("line.bin")

particles = sim.Particles(nparticles=1)
particles.p0c=7000e6

sim.TrackJobCL.print_available_devices()

devices = {"NVidia TitanV":"0.0",
           "NVidia GT1030":"0.1",
           "AMD RadeonVII":"1.0",
           "AMD TR1950X": "2.0"}

def log_gen(base,steps,maxexp,extra):
    ss=set()
    for ee in np.arange(1,maxexp,1/steps):
        nn=int(base**ee)
        for ex in range(-extra,extra+1):
           res= nn+ex
           if res>0 and res not in ss:
               yield res
               ss.add(res)

# plot nturns for


out={}
for label,device in devices.items():
    out[label]=[]
    #for npart in log_gen(base=4,steps=2,maxexp=8,extra=1):
    for npart in [5000]:
        for nturn in [1,10,20,30]:
           print(label, npart,nturn)
           cljob = sim.TrackJobCL(particles, elements, device=device,dump_element=0)
           duration=speed(cljob,npart,nturn)
           out[label].append([npart,nturn,duration])
           #if duration > 1:
           #   break
    out[label]=np.array(out[label])
    out[label].dump(label+'.npy')

