import numpy as np

import simpletrack as sim

elements=sim.Elements()

elements.Multipole(knl=[0.1570796327], hxl=0.1570796327,length=1)
elements.Drift(length=5)
elements.Multipole(knl=[0, 0.1657145946])
elements.Drift(length=5)
elements.Multipole(knl=[0.1570796327], hxl=0.1570796327,length=1)
elements.Drift(length=5)
elements.Multipole(knl=[0, -0.1685973315] )
elements.Drift(length=5)
elements.Cavity(voltage=5000000.0, frequency=239833966.4, lag=180)
elements.Monitor(turns=10)

particles=sim.Particles(nparticles=5)
particles.p0c=450e9
particles.x=np.linspace(0,1e-8,5)

job=sim.TrackJobCL(particles, elements)
job.track(10)
job.collect()

job.monitor[0].x.reshape(5,-1)





