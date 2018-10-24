import sys

import numpy as np

import simpletrack as sim

elements = sim.Elements()
elements.Drift(length=1)
elements.Drift(length=2)
elements.Drift(length=3)

particles = sim.Particles(nparticles=11)
particles.px=np.linspace(0,0.001,particles.nparticles)

cljob = sim.TrackJobCL(particles, elements, device="0.0",dump_element=5)
cljob.track(5)
cljob.collect()

np=particles.nparticles
ne=3
nt=5
particle=3
element=1
turn=4

data=cljob.dump_element.x.reshape(np,ne,nt)[particle,element,turn]

assert data==0.0075

