import sixtracktools
import pysixtrack
import simpletrack as sim

elements=sim.Elements()

six = sixtracktools.SixInput(".")
line = pysixtrack.Line.from_sixinput(six,classes=elements.gen_builder_class())

elements.tofile('line.bin')


