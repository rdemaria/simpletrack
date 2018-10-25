import sys

import numpy as np

import simpletrack as sim

elements = sim.Elements()
elements.Monitor(turns=5)
elements.Drift(length=1.2)
elements.Multipole(knl=[0,0.8])
elements.Monitor(turns=5)
elements.Drift(length=1.2)
m=elements.Multipole(knl=[0,-0.7])

elements.tofile('fodo.buf')
elements = sim.Elements.fromfile('fodo.buf')

particles = sim.Particles(nparticles=11)
particles.px=np.linspace(0,0.001,particles.nparticles)

cljob = sim.TrackJobCL(particles, elements,
                       device="0.0",dump_element=5)
cljob.track(5)
cljob.collect()


np=11
nt=5
particle=2
turn=3

def test_monitor():
  assert(cljob.monitor[0].x.reshape(np,nt)[particle][1]==2.49600000e-04)

