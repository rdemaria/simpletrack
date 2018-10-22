#include "common/buffer.h"
#include "opencl/particlecl.h"
#include "opencl/elementscl.h"

#include "common/aperture.h"
#include "common/drift.h"
#include "common/multipole.h"
#include "common/cavity.h"
#include "common/align.h"

__kernel void track(__global slot_t *particles_p,
                    __global slot_t *elements_p,
                    long nelems,
//                    __global slot_t *output_p,
                    long nturns,
                    long nturns_ebe){


    // Setup Elements
    __global Object * element = get_element_pointer(elements_p);
    size_t base = get_base(elements_p);
    type_t elemtype;
    __global slot_t * elem_p;

    // Setup particle
    size_t partid = get_global_id(0);
    Particle particle;
    copy_particle_from(particles_p, partid, &particle);

    // Track
    for (int iturn=0; iturn<nturns; iturn++){
        for (size_t ielem=0; ielem<nelems; ielem++){
            if (particle.islost>=0){
              elemtype = element[ielem].type;
              elem_p = &elements_p[(element[ielem].address-base)/8];
              switch (elemtype){
                case DriftID:
                  Drift_track((__global Drift *) elem_p, &particle);
                  if (check_bounds(&particle,1.0)) particle.islost=-ielem;
                  break;
                case DriftExactID:
                  DriftExact_track((__global Drift *) elem_p, &particle);
                  if (check_bounds(&particle,1.0)) particle.islost=-ielem;
                  break;
                case MultipoleID:
                  Multipole_track((__global Multipole *) elem_p, &particle);
                  break;
                case CavityID:
                  Cavity_track((__global Cavity *) elem_p, &particle);
                  break;
                case XYShiftID:
                  XYShift_track((__global XYShift *) elem_p, &particle);
                  break;
                case SRotationID:
                  SRotation_track((__global SRotation *) elem_p, &particle);
                  break;
              };
            } else {
                break;
            };
        };
        if (particle.islost>=0) {particle.turns++;}  else  break; ;
    };

    // Copy back
    copy_particle_to(particles_p, partid, &particle);
};

