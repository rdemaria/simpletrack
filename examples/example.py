import simpletrack as sim

# create particles
npart=100
particles = sim.Particles(nparticles=npart)

# alternate API
elements = sim.Elements()
sim.Drift(elements, length=1.0)
sim.Drift(elements, length=2.0)
sim.Drift(elements, length=3.0)
#line=sim.Line(elements)


# OpenCL workflow
sim.TrackJobCL.print_devices()
cljob = sim.TrackJobCL(particles, elements, device="0.0")
cljob.track(nturns=10)
cljob.collect()

cljob.track(nturns=10, nturns_ebe=10)
cljob.track(nturns=10, nturns_ebe=10)
cljob.track(nturns=10, nturns_ebe=10)
trackout = clctx.collect()

# tracking
job = sim.TrackJob(line, particles)
job = job.track(nturns, nturns_ebe=10)
job = job.track(nturns, nturns_ebe=10)
job = job.track(nturns, nturns_ebe=10)

# CUDA workflow
cudajob = sim.TrackJobCL(device="0", line, particles)
cudajob.track(nturns, nturns_ebe=10)
cudajob.track(nturns, nturns_ebe=10)
cudajob.track(nturns, nturns_ebe=10)
cudajob.track(nturns, nturns_ebe=10)
cudajob = cudactx.collect()

# HTCondor workflow
htjob = sim.HTContext(queue, line, particles))
htjob = track(nturns, nturns_ebe = 10)
htjob = track(nturns, nturns_ebe = 10)
htjob = track(nturns, nturns_ebe = 10)
htjob = collect()
