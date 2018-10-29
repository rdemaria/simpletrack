import numpy as np

from cobjects import CBuffer, CObject, CField

_factorial = np.array([1,
                       1,
                       2,
                       6,
                       24,
                       120,
                       720,
                       5040,
                       40320,
                       362880,
                       3628800,
                       39916800,
                       479001600,
                       6227020800,
                       87178291200,
                       1307674368000,
                       20922789888000,
                       355687428096000,
                       6402373705728000,
                       121645100408832000,
                       2432902008176640000])


_clight = 299792458


class Line(CObject):
    _typeid = 0
    n_elements = CField(0, "int64", const=True)
    elements = CField(1, "int64", length="n_elements")

    def __init__(self, cbuffer, elements=None):
        if elements is None:
            elements = np.arange(cbuffer.n_objects, dtype="int64")
        CObject.__init__(self,
                         n_elements=len(elements),
                         elements=elements)


class Drift(CObject):
    _typeid = 2
    length = CField(0, "float64", default=0.0,)


class DriftExact(CObject):
    _typeid = 3
    length = CField(0, 'float64', default=0.0)


class Multipole(CObject):
    _typeid = 4
    order = CField(0, 'int64',   const=True, default=0)
    length = CField(1, 'float64',    default=0.0)
    hxl = CField(2, 'float64',    default=0.0)
    hyl = CField(3, 'float64',    default=0.0)
    bal = CField(4, 'float64',    default=0.0,
                 length='2 * order + 2')

    def __init__(self, knl=None, ksl=None, order=None, bal=None, **nargs):
        if knl is None:
            knl = []
        if ksl is None:
            ksl = []
        if order is None:
            if bal is None:
                order = max(len(knl), len(ksl)-1)
            else:
                order = len(bal)//2-1
        nbal = np.zeros(2*order+2, dtype=float)
        if bal is None:
            nbal[:len(knl)*2:2] = knl
            nbal[1:len(ksl)*2:2] = ksl
            nbal[::2] /= _factorial[:order+1]
            nbal[1::2] /= _factorial[:order+1]
        else:
            nbal[:len(bal)] = bal
        CObject.__init__(self, order=order, bal=nbal, **nargs)


class RFMultipole(CObject):
    _typeid = 10
    order = CField(0, 'int64',   const=True, default=0)
    length = CField(1, 'float64',    default=0.0)
    bal = CField(2, 'float64',    default=0.0,
                 length='4 * order + 2')

    def __init__(self,
                 knl=None, ksl=None,
                 phn=None, phs=None,
                 order=None, bal=None, **nargs):
        if order is None:
            if bal is None:
                order = max(len(knl), len(ksl))-1
            else:
                order = len(bal)//4-1
        nbal = np.zeros(4*order+2, dtype=float)
        if bal is None:
            nbal[:len(knl)*2:4] = knl
            nbal[1:len(ksl)*2:4] = ksl
            nbal[::4] /= factorial[:order+1]
            nbal[1::4] /= factorial[:order+1]
            nbal[3:len(phn)*2:4] = phn
            nbal[4:len(phs)*2:4] = phs
        else:
            nbal[:len(bal)] = bal
        CObject.__init__(self, order=order, length=length,
                         hxl=hxl, hyl=hyl, bal=nbal, **nargs)


class Cavity(CObject):
    _typeid = 5
    voltage = CField(0, 'float64', default=0.0)
    kfreq = CField(1, 'float64', default=0.0)
    phase = CField(2, 'float64', default=0.0)

    def __init__(self, voltage=0.0, frequency=0, lag=0, **nargs):
        kfreq = 2*np.pi*frequency/_clight
        phase = lag/180*np.pi
        CObject.__init__(self,
                         voltage=voltage,
                         kfreq=kfreq,
                         phase=phase, **nargs)


class XYShift(CObject):
    _typeid = 6
    dx = CField(0, 'float64',   default=0.0)
    dy = CField(1, 'float64',   default=0.0)


class SRotation(CObject):
    _typeid = 7
    cos_z = CField(0, 'float64',   default=1.0)
    sin_z = CField(1, 'float64',   default=0.0)

    def __init__(self, angle=0, **nargs):
        anglerad = angle/180*np.pi
        cos_z = np.cos(anglerad)
        sin_z = np.sin(anglerad)
        CObject.__init__(self,
                         cos_z=cos_z, sin_z=sin_z,**nargs)


class BeamBeam4D(CObject):
    _typeid = 8
    size = CField(0, 'uint64', default=0)
    data = CField(1, 'float64',   default=0.0,
                  length='size', pointer=True)

    def __init__(self, data, **kwargs):
        CObject.__init__(self, size=len(data), data=data, **kwargs)


class BeamBeam6D(CObject):
    _typeid = 9
    size = CField(0, 'uint64', const=True, default=0)
    data = CField(1, 'float64',   default=0.0,
                  length='size', pointer=True)

    def __init__(self, data, **kwargs):
        CObject.__init__(self, size=len(data), data=data, **kwargs)


class Monitor(CObject):
    _typeid = 10
    turns = CField(0, 'int64', default=0)
    start = CField(1, 'int64', default=0)
    skip = CField(2, 'int64', default=1)
    rolling = CField(3, 'int64', default=0)
    ref = CField(4, 'int64', default=0)


class Elements(object):
    element_types = {'Cavity': Cavity,
                     'Drift': Drift,
                     'DriftExact': DriftExact,
                     'Multipole': Multipole,
                     'RFMultipole': RFMultipole,
                     'SRotation': SRotation,
                     'XYShift': XYShift,
                     'BeamBeam6D': BeamBeam6D,
                     'BeamBeam4D': BeamBeam4D,
                     'Line': Line,
                     'Monitor': Monitor,
                     }

    def _mk_fun(self, buff, cls):
        def fun(*args, **nargs):
            #print(cls.__name__,nargs)
            return cls(cbuffer=buff, **nargs)
        return fun

    @classmethod
    def fromfile(cls, filename):
        cbuffer = CBuffer.fromfile(filename)
        return cls(cbuffer=cbuffer)

    @classmethod
    def fromline(cls,line):
        self=cls()
        for label, element_name, element in line:
            getattr(self,element_name)(**element._asdict())
        return self

    def tofile(self, filename):
        self.cbuffer.tofile(filename)

    def __init__(self, cbuffer=None):
        if cbuffer is None:
            self.cbuffer = CBuffer()
        else:
            self.cbuffer = cbuffer
        for name, cls in self.element_types.items():
            setattr(self, name, self._mk_fun(self.cbuffer, cls))
            self.cbuffer.typeids[cls._typeid] = cls

    def gen_builder(self):
        out = {}
        for name, cls in self.element_types.items():
            out[name] = getattr(self, name)
        return out

    def set_monitors(self,offset=0):
        monitorid = self.element_types['Monitor']._typeid
        monitors = []
        nmonitor = 0
        for i in range(self.cbuffer.n_objects):
            if self.cbuffer.get_object_typeid(i) == monitorid:
                monitor = self.cbuffer.get_object(i)
                monitor.ref = nmonitor+offset
                monitors.append(monitor)
                nmonitor += 1
        return monitors

    def get_elements(self):
        n = self.cbuffer.n_objects
        return [self.cbuffer.get_object(i) for i in range(n)]

    def get(self,objid):
        return self.cbuffer.get_object(objid)
