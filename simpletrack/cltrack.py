import os

import numpy as np
import pyopencl

from .particles import ParticlesSet

modulepath = os.path.dirname(os.path.abspath(__file__))
os.environ['PYOPENCL_COMPILER_OUTPUT'] = "1"
srcpath = '-I%s' % modulepath

mf = pyopencl.mem_flags
clrw = mf.READ_WRITE | mf.COPY_HOST_PTR
clwo = mf.WRITE_ONLY | mf.COPY_HOST_PTR
clro = mf.READ_ONLY | mf.COPY_HOST_PTR


class TrackJobCL(object):
    @classmethod
    def print_devices(cls):
        for np, platform in enumerate(pyopencl.get_platforms()):
            print(f"{np}: {platform.name}")
            for nd, device in enumerate(platform.get_devices()):
                print(f"{np}.{nd}: {device.name}")

    def build_program(self, src="track.c"):
        src = open(os.path.join(modulepath, 'opencl', src)).read()
        options = [srcpath]
        self.program = pyopencl.Program(self.ctx, src).build(options=options)

    def create_context(self, device):
        np, nd = map(int, device.split('.'))
        platform = pyopencl.get_platforms()[np]
        device = platform.get_devices()[nd]
        self.ctx = pyopencl.Context([device])
        self.queue = pyopencl.CommandQueue(self.ctx)
        self.build_program()

    def __init__(self, particles, elements, device='0.0', dump_element=0):
        # self.line=line
        self.create_context(device)
        self._set_particles(particles)
        self._set_elements(elements)
        self.set_output(dump_element)


    def _set_particles(self,particles):
        self.particles = particles
        self.particles_buf = self.particles._get_slot_buffer()
        self.particles_g = pyopencl.Buffer(self.ctx, clrw,
                                           hostbuf=self.particles_buf)
        self.npart = np.int64(self.particles.nparticles)

    def set_particles(self,particles):
        old_npart=self.npart
        self._set_particles(particles)
        if self.particles.nparticles!=old_npart:
            self.set_output(self.dump_element_turns)


    def _set_elements(self,elements):
        self.elements = elements
        self.elements_buf = self.elements.buffer._data_i64
        self.elements_g = pyopencl.Buffer(self.ctx, clro,
                                          hostbuf=self.elements_buf)
        self.nelems = np.int64(self.elements.buffer.n_objects)

    def set_elements(self,elements):
        old_nmonitor=self.nmonitor
        self._set_elements(elements)
        if self.nmonitor!=old_nmonitor:
            self.set_output(self.dump_element_turns)

    def set_output(self, turns):
        output=ParticlesSet()

        #Element DUMP
        self.dump_element_turns = np.int64(turns)
        size=self.nelems*self.npart*turns
        self.dump_element = output.Particles(nparticles=size,partid=-1)

        # GPU preparation
        self.output_buf = output.buffer._data_i64
        self.output_g = pyopencl.Buffer(self.ctx, clrw,
                                              hostbuf=self.output_buf)
    def check_output(self,dump_element_turns):
        if not hasattr(self,'output_buf'):
            self.set_output(dump_element_turns)

    def track(self, turns=1):
        """
        turns -> max number of turns
        """
        turns = np.int64(turns)
        self.set_output(self.dump_element_turns)
        self.program.track(self.queue, [self.npart], None,
                           self.particles_g,
                           self.output_g,
                           self.elements_g, self.nelems,
                           turns, self.dump_element_turns)

    def collect(self):
        pyopencl.enqueue_copy(self.queue,
                              self.particles_buf,
                              self.particles_g)
        pyopencl.enqueue_copy(self.queue,
                              self.output_buf,
                              self.output_g)
