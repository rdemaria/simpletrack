import simpletrack as sim


# alternate API
elements = sim.Elements()
sim.Drift(elements, length=1.0)
sim.Drift(elements, length=2.0)
sim.Drift(elements, length=3.0)
#line=sim.Line(elements)

# create particles
npart=1
particles = sim.Particles(nparticles=npart)
particles.px=0.001

# OpenCL workflow
sim.TrackJobCL.print_devices()
cljob = sim.TrackJobCL(particles, elements, device="0.0",dump_element=5)
cljob.track(nturns=10)
cljob.collect()

cljob.dump_element.x

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
