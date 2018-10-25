#include "common/buffer.h"
#include "common/particle.h"

#define PARTICLE Particle *
#define PARTICLE_GET(p,name) p->name
#define REAL(name) double name
#define INT(name) long name

/*! python
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

/* python
import simpletrack as sim
sim.Particles._gen_opencl_copyparticle()
*/
void copy_particle_from(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle){
      size_t npart =particles_p[0].i64;
      particle->mass0   =particles_p[2+0*npart+partid].f64 ;
      particle->p0c     =particles_p[2+1*npart+partid].f64 ;
      particle->beta0   =particles_p[2+2*npart+partid].f64 ;
      particle->charge0 =particles_p[2+3*npart+partid].f64 ;
      particle->x       =particles_p[2+4*npart+partid].f64 ;
      particle->px      =particles_p[2+5*npart+partid].f64 ;
      particle->y       =particles_p[2+6*npart+partid].f64 ;
      particle->py      =particles_p[2+7*npart+partid].f64 ;
      particle->zeta    =particles_p[2+8*npart+partid].f64 ;
      particle->delta   =particles_p[2+9*npart+partid].f64 ;
      particle->rpp     =particles_p[2+10*npart+partid].f64 ;
      particle->rvv     =particles_p[2+11*npart+partid].f64 ;
      particle->rmass   =particles_p[2+12*npart+partid].f64 ;
      particle->rcharge =particles_p[2+13*npart+partid].f64 ;
      particle->chi     =particles_p[2+14*npart+partid].f64 ;
      particle->partid  =particles_p[2+15*npart+partid].i64 ;
      particle->turns   =particles_p[2+16*npart+partid].i64 ;
      particle->islost  =particles_p[2+17*npart+partid].i64 ;
};
void copy_particle_to(__global slot_t *particles_p,
                   size_t partid,
                   Particle *particle){
      size_t npart =particles_p[0].i64;
      particles_p[2+0*npart+partid].f64= particle->mass0  ;
      particles_p[2+1*npart+partid].f64= particle->p0c    ;
      particles_p[2+2*npart+partid].f64= particle->beta0  ;
      particles_p[2+3*npart+partid].f64= particle->charge0;
      particles_p[2+4*npart+partid].f64= particle->x      ;
      particles_p[2+5*npart+partid].f64= particle->px     ;
      particles_p[2+6*npart+partid].f64= particle->y      ;
      particles_p[2+7*npart+partid].f64= particle->py     ;
      particles_p[2+8*npart+partid].f64= particle->zeta   ;
      particles_p[2+9*npart+partid].f64= particle->delta  ;
      particles_p[2+10*npart+partid].f64= particle->rpp    ;
      particles_p[2+11*npart+partid].f64= particle->rvv    ;
      particles_p[2+12*npart+partid].f64= particle->rmass  ;
      particles_p[2+13*npart+partid].f64= particle->rcharge;
      particles_p[2+14*npart+partid].f64= particle->chi    ;
      particles_p[2+15*npart+partid].i64= particle->partid ;
      particles_p[2+16*npart+partid].i64= particle->turns  ;
      particles_p[2+17*npart+partid].i64= particle->islost ;
};
/* end python*/


int check_is_notlost(Particle *const particle_p){
    return particle_p->islost>=0;
};

int increase_turn(Particle *const particle_p){
    return particle_p->turns++;
};
