#!/usr/bin/env python3

import time, sys

import numpy as np

import sixtracktools
import simpletrack as sim
import pysixtrack


npart=1
nturns=1
x0=0.0001

particles = sim.Particles(nparticles=npart)
particles.p0c=7000e9
particles.x=x0

#lhc = sixtracktools.SixInput('.')
#line, rest, iconv = lhc.expand_struct()
#elements=sim.Elements.fromline(line)

elements=sim.Elements()
lhc = sixtracktools.SixInput('.')
line, rest, iconv = lhc.expand_struct(convert=elements.gen_builder())

#elements.Monitor(turns=nturns)

cljob = sim.TrackJobCL(particles, elements, device="0.0",dump_element=nturns)
cljob.track()
cljob.collect()
out=cljob.dump_element

refline, rest, iconv = lhc.expand_struct(convert=pysixtrack.element_types)
refline= pysixtrack.Line(elements=[l[2] for l in refline ])


prun=pysixtrack.Particles(p0c=7000e9,x=x0)
refout=refline.track_elem_by_elem(prun)

refx=np.array([p.x for p in refout])

