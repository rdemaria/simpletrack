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

device="0.0"
npart=20000
nturn=15

for device in sim.TrackJobCL.get_available_devices():
    cljob = sim.TrackJobCL(particles, elements, device=device,dump_element=0)
    duration=speed(cljob,npart,nturn)
    print(f"device '{device}', {npart} particles, {nturn} turns,"
        f" {(npart*nturn)/duration:.0f} particles*turns/seconds, {cljob.ctx.devices[0].name}")
