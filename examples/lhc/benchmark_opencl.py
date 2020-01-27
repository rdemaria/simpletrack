#!/usr/bin/env python3

import time, sys, argparse

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

parser = argparse.ArgumentParser(description='Simpletrack benchmark')
parser.add_argument('-d','--device',dest='device',default='0.0',help='OpenCL device to use')
parser.add_argument('-p','--particles',dest='npart',type=int,default=20000,help='Number of particles')
parser.add_argument('-t','--turns',dest='nturn',type=int,default=15,help='Number of turns')
parser.add_argument('-s','--show',dest='show',action='store_true',help='List available devices')

args = parser.parse_args()

if (args.show):
  sim.TrackJobCL.print_available_devices()

else:
  for args.device in sim.TrackJobCL.get_available_devices():
    cljob = sim.TrackJobCL(particles, elements, device=args.device,dump_element=0)   
    duration=speed(cljob,args.npart,args.nturn)
    print( f"{(args.npart*args.nturn)/duration:9.0f} particles*turns/seconds, "
          f"{args.npart} particles, {args.nturn} turns, "
          f"device '{args.device}', {cljob.ctx.devices[0].name}")
