#include "common/buffer.h"
#include "opencl/particlecl.h"
#include "opencl/buffercl.h"

#include "common/aperture.h"
#include "common/drift.h"
#include "common/multipole.h"
#include "common/cavity.h"
#include "common/align.h"
#include "common/monitor.h"
#include "common/elements.h"
#include "common/track.h"


__kernel void track(__global slot_t *particles_p,
                    __global slot_t *output_p,
                    __global slot_t *elements_p,
                    long nelems,
                    long nturns,
                    long dump_element_nturns){

    // Setup particle
    size_t partid = get_global_id(0);

    // Copy to private
    Particle particle;
    Particle *const particle_p=&particle;
    copy_particle_from(particles_p, partid, particle_p);

    //Track
    track_loop(particle_p, output_p, elements_p,
               nelems, nturns, dump_element_nturns);

    // Copy back
    copy_particle_to(particles_p, partid, particle_p);
};

