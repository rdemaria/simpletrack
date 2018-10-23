import numpy as np

import sixtracktools
import simpletrack as sim

elem=sim.ElementBuilder()
elem.gen_builder()

six = sixtracktools.SixInput('.')
line, rest, iconv = six.expand_struct(convert=elem.gen_builder())
sixdump = sixtracktools.SixDump101('res/dump3.dat')[::2]
elements=elem.elements


npart=60
particles = sim.Particles(nparticles=npart)
particles.p0c=7000e6
particles.px=np.linspace(0,0.0001,npart)

sim.TrackJobCL.print_devices()
cljob = sim.TrackJobCL(particles, elements, device="0.0",dump_element=0)
import time;start=time.time()
cljob.track(1000);cljob.collect()
print(time.time()-start)




def compare(prun,pbench):
    out=[]
    for att in 'x px y py delta sigma'.split():
        vrun=getattr(prun,att)
        vbench=getattr(pbench,att)
        diff=vrun-vbench
        out.append(abs(diff))
        print(f"{att:<5} {vrun:22.13e} {vbench:22.13e} {diff:22.13g}")
    print(f"max {max(out):21.12e}")
    return max(out)

print("")
for ii in range(1,len(iconv)):
    jja=iconv[ii-1]
    jjb=iconv[ii]
    prun=pysixtrack.Particles(**sixdump[ii-1].get_minimal_beam())
    print(f"\n-----sixtrack={ii} sixtracklib={jja} --------------")
    #print(f"pysixtr {jja}, x={prun.x}, px={prun.px}")
    for jj in range(jja+1, jjb+1):
        label,elem_type,elem=line[jj]
        elem.track(prun)
        print(f"{jj} {label},{str(elem)[:50]}")
    pbench=pysixtrack.Particles(**sixdump[ii].get_minimal_beam())
    #print(f"sixdump {ii}, x={pbench.x}, px={pbench.px}")
    print("-----------------------")
    out=compare(prun,pbench)
    print("-----------------------\n\n")
    if out>1e-13:
        print("Too large discrepancy")
        break


