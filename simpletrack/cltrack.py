import os

import numpy as np
import pyopencl

from .particles import Particles

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
        self.elements = elements
        self.particles = particles
        self.create_context(device)
        self.prepare_buffers()
        self.set_dump_element(dump_element)

    def prepare_buffers(self):
        self.particles_buf = self.particles._get_buffer().view('uint64')
        self.particles_g = pyopencl.Buffer(self.ctx, clrw,
                                           hostbuf=self.particles_buf)
        self.elements_buf = self.elements._data_i64
        self.elements_g = pyopencl.Buffer(self.ctx, clro,
                                          hostbuf=self.elements_buf)
        self.nelems = np.int64(self.elements.n_objects)
        self.npart = np.int64(self.particles.nparticles)

    def set_dump_element(self, nturns):
        self.dump_element_nturns = np.int64(nturns)
        size=self.nelems*self.npart*nturns
        self.dump_element = Particles(nparticles=size)
        self.dump_element_buf = self.dump_element._get_buffer().view('uint64')
        self.dump_element_g = pyopencl.Buffer(self.ctx, clrw,
                                              hostbuf=self.dump_element_buf)

    def track(self, nturns=1):
        nturns = np.int64(nturns)
        self.program.track(self.queue, [self.npart], None,
                           self.particles_g,
                           self.dump_element_g,
                           self.elements_g, self.nelems,
                           nturns, self.dump_element_nturns)

    def collect(self):
        pyopencl.enqueue_copy(self.queue,
                              self.particles_buf,
                              self.particles_g)
        pyopencl.enqueue_copy(self.queue,
                              self.dump_element_buf,
                              self.dump_element_g)
