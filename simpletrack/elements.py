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


clight = 299792458

def Elements():
    return CBuffer()

class Line(CObject):
    _typeid=0
    n_elements=CField(0,"int64",const=True)
    elements=CField(1,"int64",length="n_elements")
    def __init__(self,cbuffer,elements=None):
        if elements is None:
            elements=np.arange(cbuffer.n_objects,dtype="int64")
        CObject.__init__(self,
                             n_elements=len(elements),
                             elements=elements)

class Drift(CObject):
    _typeid=2
    length=CField(0,"float64", default=0.0,)

class DriftExact( CObject ):
    _typeid = 3
    length  = CField( 0, 'float64', default=0.0 )

class MultiPole( CObject ):
    _typeid = 4
    order   = CField( 0, 'int64',   default=0 )
    length  = CField( 1, 'float64',    default=0.0 )
    hxl     = CField( 2, 'float64',    default=0.0 )
    hyl     = CField( 3, 'float64',    default=0.0 )
    bal     = CField( 4, 'float64',    default=0.0,
                      length='2 * order + 2')
    def __init__(self, cbuffer=None, knl=None, ksl=None, order=None, bal=None,
                                     hxl=0, hyl=0, length=0):
        if order is None:
            if bal is None:
               order=max(len( knl ), len( ksl ))-1
            else:
               order=len(bal)//2-1
        nbal=np.zeros(2*order+2, dtype=float)
        if bal is None:
            nbal[:len(knl)*2:2]=knl
            nbal[1:len(ksl)*2:2]=ksl
            nbal[::2]/=factorial[:order+1]
            nbal[1::2]/=factorial[:order+1]
        else:
            nbal[:len(bal)]=bal
        CObject.__init__(self, cbuffer=cbuffer, order=order, length=length,
                               hxl=hxl, hyl=hyl, bal=nbal)


class Cavity( CObject ):
    _typeid = 5
    voltage  = CField( 0, 'float64', default=0.0 )
    kfreq    = CField( 1, 'float64', default=0.0 )
    phase    = CField( 2, 'float64', default=0.0 )

    def __init__(self, cbuffer=None, voltage=0.0, frequency = 0, lag=0):
        kfreq=2*np.pi*frequency/clight
        phase = lag/180*pi
        CObject.__init__(self, cbuffer=cbuffer,
                         voltage=voltage,
                         kfreq = kfreq,
                         phase =phase)


class XYShift( CObject ):
    _typeid = 6
    dx      = CField( 0, 'float64',   default=0.0 )
    dy      = CField( 1, 'float64',   default=0.0 )

class SRotation( CObject ):
    _typeid = 7
    cos_z   = CField( 0, 'float64',   default=1.0 )
    sin_z   = CField( 1, 'float64',   default=0.0 )

    def __init__(self,cbuffer=None, angle=0):
        anglerad=angle/180*np.pi
        cos_z=np.cos(angle)
        sin_z=np.sin(angle)
        CObject.__init__( self,cbuffer=cbuffer, cos_z=cos_z, sin_z=sin_z)


class BeamBeam4D( CObject ):
    _typeid = 8
    size     = CField( 0, 'uint64', default=0 )
    data     = CField( 1, 'float64',   default=0.0,
                      length='size', pointer=True )
    def __init__(self, data, **kwargs):
        CObject.__init__( self, size=len(data), data=data, **kwargs)


class BeamBeam6D( CObject ):
    _typeid = 9
    size     = CField( 0, 'uint64', default=0 )
    data     = CField( 1, 'float64',   default=0.0,
                      length='size', pointer=True )
    def __init__(self, data, **kwargs):
        CObject.__init__( self, size=len(data), data=data, **kwargs)



