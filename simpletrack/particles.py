from cobjects import CObject, CField


## chi = q/q_0 m_0/m
## rmass = m_0/m
## rchange = q/q_0
## px = P/P0 m_0 / m

class Particles(CObject):
    pmass=938.272046e6
    _typeid=0
    nparticles=CField(0,'int64',const=True)
    x      =CField( 1,'float64',length='nparticles',default=0)
    px     =CField( 2,'float64',length='nparticles',default=0)
    y      =CField( 3,'float64',length='nparticles',default=0)
    py     =CField( 4,'float64',length='nparticles',default=0)
    zeta   =CField( 5,'float64',length='nparticles',default=0)
    delta  =CField( 6,'float64',length='nparticles',default=0)
    rpp    =CField( 7,'float64',length='nparticles',default=1)
    rvv    =CField( 8,'float64',length='nparticles',default=1)
    mass0  =CField(10,'float64',length='nparticles',default=pmass)
    p0c    =CField(10,'float64',length='nparticles',default=1e9)
    beta0  =CField( 9,'float64',length='nparticles',default=1)
    charge0=CField(11,'float64',length='nparticles',default=1)
    rmass  =CField(12,'float64',length='nparticles',default=1)
    rcharge=CField(13,'float64',length='nparticles',default=1)
    chi    =CField(14,'float64',length='nparticles',default=1)
    turns  =CField(15,'int64',length='nparticles',default=0)
    islost =CField(16,'int64',length='nparticles',default=0)

    @classmethod
    def _gen_opencl_copyparticle(cls):
        types={'float64':'f64','int64':'i64'}
        out=["""void copy_particle_from(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle){
      size_t npart =particles_p[0].i64;"""]
        for name,field in cls.get_fields():
            if field.index>0:
                ctype=f"{types[field.ftype]}"
                data=f"particles_p[1+{field.index-1}*npart+partid]"
                out.append(f"      particle->{name:7} ={data}.{ctype} ;")
        out.append('};')
        print('\n'.join(out))
        out=["""void copy_particle_to(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle){
      size_t npart =particles_p[0].i64;"""]
        for name,field in cls.get_fields():
            if field.index>0:
                ctype=f"{types[field.ftype]}"
                data=f"particles_p[1+{field.index-1}*npart+partid]"
                out.append(f"      {data}.{ctype}= particle->{name:7};")
        out.append('};')
        print('\n'.join(out))

    @classmethod
    def _gen_opencl_particle_type(cls):
        types={'float64':'double','int64':'long'}
        out=["typedef struct {"]
        for name,field in cls.get_fields():
            if field.index>0:
                out.append(f"    {types[field.ftype]} {name};")
        out.append('} Particle;')
        out.append("\n#define PARTICLE_GET(p,name) p.name")
        print('\n'.join(out))

    @classmethod
    def _gen_common_particle_slots(cls):
        types={'float64':'REAL','int64':'INT'}
        out=['#define PARTICLE_SLOTS  \\']
        for name,field in cls.get_fields():
            if field.index>0:
                ctype=types[field.ftype]
                cdef=f" {ctype}({name});"
                out.append(f"  {cdef:23}\\")
        print('\n'.join(out))

    @classmethod
    def _gen_common_particle_accessors(cls):
        out=[]
        for name,field in cls.get_fields():
            if field.index>0:
                fdef=f"#define {name.upper()}(p)"
                out.append(f"{fdef:18} PARTICLE_GET(p,{name})")
        print('\n'.join(out))

