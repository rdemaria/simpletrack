import simpletrack as sim

# alternate API
elem = sim.Elements()
elem.Drift(length=1.0)
elem.Drift(length=2.0)
elem.Drift(length=3.0)
#line=sim.Line(elements)

# create particles
npart=1
part = sim.Particles(nparticles=npart)
part.px=0.001

# OpenCL workflow
sim.TrackJobCL.print_devices()
cljob = sim.TrackJobCL(part, elem, device="0.0",dump_element=5)
cljob.track(turns=10)
cljob.collect()


cljob.dump_element.x

## to do

cljob.track(turns=10)
cljob.track(turns=20)
cljob.track(turns=30)
trackout = clctx.collect()

# tracking
job = sim.TrackJob(line, particles)
job = job.track(turns)
job = job.track(turns)
job = job.track(turns)

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
