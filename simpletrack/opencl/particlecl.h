#include "common/buffer.h"
#include "common/particle.h"

#define PARTICLE(name) Particle * const name
#define PARTICLE_GET(p,name) p->name
#define REAL(name) double name
#define INT(name) long name

/*! code_gen python
import simpletrack as sim
sim.Particles._gen_opencl_particle_type()
*/
typedef struct {
    PARTICLE_SLOTS
} Particle;
/* end python */

void copy_particle_from(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle);

void copy_particle_to(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle);

/* code_gen python
import simpletrack as sim
sim.Particles._gen_opencl_copyparticle()
*/
void copy_particle_from(__global slot_t *particles_p,
                   size_t ipart,
                   Particle *particle){
      size_t npart =particles_p[0].i64;
      particle->mass0   =particles_p[1+0*npart+ipart].f64 ;
      particle->p0c     =particles_p[1+1*npart+ipart].f64 ;
      particle->beta0   =particles_p[1+2*npart+ipart].f64 ;
      particle->charge0 =particles_p[1+3*npart+ipart].f64 ;
      particle->x       =particles_p[1+4*npart+ipart].f64 ;
      particle->px      =particles_p[1+5*npart+ipart].f64 ;
      particle->y       =particles_p[1+6*npart+ipart].f64 ;
      particle->py      =particles_p[1+7*npart+ipart].f64 ;
      particle->zeta    =particles_p[1+8*npart+ipart].f64 ;
      particle->delta   =particles_p[1+9*npart+ipart].f64 ;
      particle->rpp     =particles_p[1+10*npart+ipart].f64 ;
      particle->rvv     =particles_p[1+11*npart+ipart].f64 ;
      particle->rmass   =particles_p[1+12*npart+ipart].f64 ;
      particle->rcharge =particles_p[1+13*npart+ipart].f64 ;
      particle->chi     =particles_p[1+14*npart+ipart].f64 ;
      particle->partid  =particles_p[1+15*npart+ipart].i64 ;
      particle->turns   =particles_p[1+16*npart+ipart].i64 ;
      particle->islost  =particles_p[1+17*npart+ipart].i64 ;
};
void copy_particle_to(__global slot_t *particles_p,
                   size_t ipart,
                   Particle *particle){
      size_t npart =particles_p[0].i64;
      particles_p[1+0*npart+ipart].f64= particle->mass0  ;
      particles_p[1+1*npart+ipart].f64= particle->p0c    ;
      particles_p[1+2*npart+ipart].f64= particle->beta0  ;
      particles_p[1+3*npart+ipart].f64= particle->charge0;
      particles_p[1+4*npart+ipart].f64= particle->x      ;
      particles_p[1+5*npart+ipart].f64= particle->px     ;
      particles_p[1+6*npart+ipart].f64= particle->y      ;
      particles_p[1+7*npart+ipart].f64= particle->py     ;
      particles_p[1+8*npart+ipart].f64= particle->zeta   ;
      particles_p[1+9*npart+ipart].f64= particle->delta  ;
      particles_p[1+10*npart+ipart].f64= particle->rpp    ;
      particles_p[1+11*npart+ipart].f64= particle->rvv    ;
      particles_p[1+12*npart+ipart].f64= particle->rmass  ;
      particles_p[1+13*npart+ipart].f64= particle->rcharge;
      particles_p[1+14*npart+ipart].f64= particle->chi    ;
      particles_p[1+15*npart+ipart].i64= particle->partid ;
      particles_p[1+16*npart+ipart].i64= particle->turns  ;
      particles_p[1+17*npart+ipart].i64= particle->islost ;
};
/* end python*/


int check_is_notlost(Particle *const particle_p){
    return particle_p->islost>=0;
};

int increase_turn(Particle *const particle_p){
    return particle_p->turns++;
};



void copy_particle_to_dump_element(
                 ELEMENT_MEM slot_t *dump_elements_p,
                 PARTICLE(particle_p),
                 size_t ielem, size_t nelems,
                 size_t dump_element_nturns
                 ){
    if (particle_p->turns<dump_element_nturns){
       size_t pos=particle_p->partid*nelems*dump_element_nturns+
                   ielem*dump_element_nturns+
                   particle_p->turns;
       copy_particle_to(dump_elements_p,pos, particle_p);
    };
};
