#include "common/buffer.h"
#include "common/particle.h"


#define PARTICLE(name) Particle * const name, size_t partid
#define PARTICLE_GET(p,name) p->name[ipart]
#define REAL(name) double * restrict name
#define INT(name) long * restrict name

struct Particles {
    size_t nparticles;
    size_t nstable;
    PARTICLE_SLOTS
};



// For track
//
/* code_gen python
import simpletrack as sim
sim.Particles._gen_cpu_copyparticle()
*/
void copy_single_particle_to(slot_t * restrict part_dst_p,
                   size_t ipart_dst,
                   Particle * restrict part_src_p
                   size_t ipart_src){
      size_t npart_dst =part_dst_p[0].i64;
      size_t npart_src =part_src_p[0].i64;
      part_dst_p[1+0*npart_dst+ipart_dst] =
      part_src_p[1+0*npart_src+ipart_src] ;
      part_dst_p[1+1*npart_dst+ipart_dst] =
      part_src_p[1+1*npart_src+ipart_src] ;
      part_dst_p[1+2*npart_dst+ipart_dst] =
      part_src_p[1+2*npart_src+ipart_src] ;
      part_dst_p[1+3*npart_dst+ipart_dst] =
      part_src_p[1+3*npart_src+ipart_src] ;
      part_dst_p[1+4*npart_dst+ipart_dst] =
      part_src_p[1+4*npart_src+ipart_src] ;
      part_dst_p[1+5*npart_dst+ipart_dst] =
      part_src_p[1+5*npart_src+ipart_src] ;
      part_dst_p[1+6*npart_dst+ipart_dst] =
      part_src_p[1+6*npart_src+ipart_src] ;
      part_dst_p[1+7*npart_dst+ipart_dst] =
      part_src_p[1+7*npart_src+ipart_src] ;
      part_dst_p[1+8*npart_dst+ipart_dst] =
      part_src_p[1+8*npart_src+ipart_src] ;
      part_dst_p[1+9*npart_dst+ipart_dst] =
      part_src_p[1+9*npart_src+ipart_src] ;
      part_dst_p[1+10*npart_dst+ipart_dst] =
      part_src_p[1+10*npart_src+ipart_src] ;
      part_dst_p[1+11*npart_dst+ipart_dst] =
      part_src_p[1+11*npart_src+ipart_src] ;
      part_dst_p[1+12*npart_dst+ipart_dst] =
      part_src_p[1+12*npart_src+ipart_src] ;
      part_dst_p[1+13*npart_dst+ipart_dst] =
      part_src_p[1+13*npart_src+ipart_src] ;
      part_dst_p[1+14*npart_dst+ipart_dst] =
      part_src_p[1+14*npart_src+ipart_src] ;
      part_dst_p[1+15*npart_dst+ipart_dst] =
      part_src_p[1+15*npart_src+ipart_src] ;
      part_dst_p[1+16*npart_dst+ipart_dst] =
      part_src_p[1+16*npart_src+ipart_src] ;
      part_dst_p[1+17*npart_dst+ipart_dst] =
      part_src_p[1+17*npart_src+ipart_src] ;
};
/* end python */


void copy_particle_to_dump_element(
            slot_t *dump_elements_p,
            slot_t *particle_p,
            size_t ielem, size_t nelems, size_t dump_element_nturns){
    for (ipart=0; ipart<particle_p->stable; ipart++){
          size_t partid=PARTID(pp);
          size_t pos=particle_p->partid*nelems*dump_element_nturns+
                     ielem*dump_element_nturns+
                     particle_p->turns;
    };
    copy_particle_to(dump_elements_p, pos, particle_p, ipart);
}


int check_is_notlost(Particles *particle_p) {
    for (int ipart=0; ipart<particle_p->stable; ipart++){
        if (IS_LOST(pp)<0){
            exchange(particle_p, ipart, particle_p->stable);
            particle_p->stable--;
        };
    };
    if (particle_p->stable==0){
        return -1;//All particles lost
    } else {
        return particle_p->stable; Stable particles
    }
};

void increase_turn(Particles *particle_p) {
    for (int ipart=0; ipart<particle_p->stable; ipart++){
        TURNS(pp)++;
    };
};


