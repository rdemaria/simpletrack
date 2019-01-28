#include "common/buffer.h"
#include "common/particle.h"


#define PARTICLE(name) Particles * const name
#define PARTICLE_GET(p,name) p->name[ipart]
#define REAL(name) double * restrict name
#define INT(name) long * restrict name
#define TEMP_REAL(name) double name
#define TEMP_INT(name) long name
#define PARTICLE_SELF(pp) (slot_t *) pp, ipart

typedef struct {
    size_t nparticles;
    size_t nstable;
    PARTICLE_SLOTS
} Particles;


int setup_particles(Particles *particle_p);
int check_is_notlost(Particles *particle_p);
void exchange(Particles * particle_p, size_t src, size_t dest);


int setup_particles(Particles *particle_p) {
    particle_p->nstable=particle_p->nparticles;
    return check_is_notlost(particle_p);
};

int check_is_notlost(Particles *particle_p) {
    for (size_t ipart=0; ipart<particle_p->nstable; ipart++){
        if (ISLOST(particle_p)<0){
            exchange(particle_p, ipart, particle_p->nstable);
            particle_p->nstable--;
        };
    };
    if (particle_p->nstable==0){
        return -1;//All particles lost
    } else {
        return particle_p->nstable; //Some stable particles
    }
};


/* code_gen python
import simpletrack as sim
sim.Particles._gen_cpu_exchange()
*/
void exchange(Particles * particle_p,
              size_t src,
              size_t dest){
    slot_t temp;
    temp.f64=particle_p->mass0[dest];
    particle_p->mass0[dest]=particle_p->mass0[src];
    particle_p->mass0[src]=temp.f64;
    temp.f64=particle_p->p0c[dest];
    particle_p->p0c[dest]=particle_p->p0c[src];
    particle_p->p0c[src]=temp.f64;
    temp.f64=particle_p->beta0[dest];
    particle_p->beta0[dest]=particle_p->beta0[src];
    particle_p->beta0[src]=temp.f64;
    temp.f64=particle_p->charge0[dest];
    particle_p->charge0[dest]=particle_p->charge0[src];
    particle_p->charge0[src]=temp.f64;
    temp.f64=particle_p->x[dest];
    particle_p->x[dest]=particle_p->x[src];
    particle_p->x[src]=temp.f64;
    temp.f64=particle_p->px[dest];
    particle_p->px[dest]=particle_p->px[src];
    particle_p->px[src]=temp.f64;
    temp.f64=particle_p->y[dest];
    particle_p->y[dest]=particle_p->y[src];
    particle_p->y[src]=temp.f64;
    temp.f64=particle_p->py[dest];
    particle_p->py[dest]=particle_p->py[src];
    particle_p->py[src]=temp.f64;
    temp.f64=particle_p->zeta[dest];
    particle_p->zeta[dest]=particle_p->zeta[src];
    particle_p->zeta[src]=temp.f64;
    temp.f64=particle_p->delta[dest];
    particle_p->delta[dest]=particle_p->delta[src];
    particle_p->delta[src]=temp.f64;
    temp.f64=particle_p->rpp[dest];
    particle_p->rpp[dest]=particle_p->rpp[src];
    particle_p->rpp[src]=temp.f64;
    temp.f64=particle_p->rvv[dest];
    particle_p->rvv[dest]=particle_p->rvv[src];
    particle_p->rvv[src]=temp.f64;
    temp.f64=particle_p->rmass[dest];
    particle_p->rmass[dest]=particle_p->rmass[src];
    particle_p->rmass[src]=temp.f64;
    temp.f64=particle_p->rcharge[dest];
    particle_p->rcharge[dest]=particle_p->rcharge[src];
    particle_p->rcharge[src]=temp.f64;
    temp.f64=particle_p->chi[dest];
    particle_p->chi[dest]=particle_p->chi[src];
    particle_p->chi[src]=temp.f64;
    temp.i64=particle_p->partid[dest];
    particle_p->partid[dest]=particle_p->partid[src];
    particle_p->partid[src]=temp.i64;
    temp.i64=particle_p->turns[dest];
    particle_p->turns[dest]=particle_p->turns[src];
    particle_p->turns[src]=temp.i64;
    temp.i64=particle_p->islost[dest];
    particle_p->islost[dest]=particle_p->islost[src];
    particle_p->islost[src]=temp.i64;
};
/* end python */


// For track
//
/* code_gen python
import simpletrack as sim
sim.Particles._gen_cpu_copyparticle()
*/
void copy_particle_to(slot_t * restrict part_dst_p,
                   size_t ipart_dst,
                   slot_t * restrict part_src_p,
                   size_t ipart_src){
      size_t npart_dst =part_dst_p[0].i64;
      size_t npart_src =part_src_p[0].i64;
      part_dst_p[2+0*npart_dst+ipart_dst] =
      part_src_p[2+0*npart_src+ipart_src] ;
      part_dst_p[2+1*npart_dst+ipart_dst] =
      part_src_p[2+1*npart_src+ipart_src] ;
      part_dst_p[2+2*npart_dst+ipart_dst] =
      part_src_p[2+2*npart_src+ipart_src] ;
      part_dst_p[2+3*npart_dst+ipart_dst] =
      part_src_p[2+3*npart_src+ipart_src] ;
      part_dst_p[2+4*npart_dst+ipart_dst] =
      part_src_p[2+4*npart_src+ipart_src] ;
      part_dst_p[2+5*npart_dst+ipart_dst] =
      part_src_p[2+5*npart_src+ipart_src] ;
      part_dst_p[2+6*npart_dst+ipart_dst] =
      part_src_p[2+6*npart_src+ipart_src] ;
      part_dst_p[2+7*npart_dst+ipart_dst] =
      part_src_p[2+7*npart_src+ipart_src] ;
      part_dst_p[2+8*npart_dst+ipart_dst] =
      part_src_p[2+8*npart_src+ipart_src] ;
      part_dst_p[2+9*npart_dst+ipart_dst] =
      part_src_p[2+9*npart_src+ipart_src] ;
      part_dst_p[2+10*npart_dst+ipart_dst] =
      part_src_p[2+10*npart_src+ipart_src] ;
      part_dst_p[2+11*npart_dst+ipart_dst] =
      part_src_p[2+11*npart_src+ipart_src] ;
      part_dst_p[2+12*npart_dst+ipart_dst] =
      part_src_p[2+12*npart_src+ipart_src] ;
      part_dst_p[2+13*npart_dst+ipart_dst] =
      part_src_p[2+13*npart_src+ipart_src] ;
      part_dst_p[2+14*npart_dst+ipart_dst] =
      part_src_p[2+14*npart_src+ipart_src] ;
      part_dst_p[2+15*npart_dst+ipart_dst] =
      part_src_p[2+15*npart_src+ipart_src] ;
      part_dst_p[2+16*npart_dst+ipart_dst] =
      part_src_p[2+16*npart_src+ipart_src] ;
      part_dst_p[2+17*npart_dst+ipart_dst] =
      part_src_p[2+17*npart_src+ipart_src] ;
};
/* end python */


void copy_particle_to_dump_element(
            slot_t *dump_elements_p,
            Particles *particle_p,
            size_t ielem, size_t nelems, size_t dump_element_nturns){
    for (size_t ipart=0; ipart<particle_p->nstable; ipart++){
        size_t partid=PARTID(particle_p);
        size_t turns=TURNS(particle_p);
        size_t pos=partid*nelems*dump_element_nturns+
                   ielem*dump_element_nturns+
                   turns;
          copy_particle_to((slot_t*) dump_elements_p, pos,
                     (slot_t*) particle_p, ipart);
    };
}


void increase_turn(Particles *particle_p) {
    for (size_t ipart=0; ipart<particle_p->nstable; ipart++){
        TURNS(particle_p)++;
    };
};


