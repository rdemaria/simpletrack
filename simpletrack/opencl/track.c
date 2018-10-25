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


__kernel void track(__global slot_t *particles_p,
                    __global slot_t *output_p,
                    __global slot_t *elements_p,
                    long nelems,
                    long nturns,
                    long dump_element_nturns){


    // Setup Elements
    __global Object *element = get_objects(elements_p);
    size_t elem_base = get_base(elements_p);
    type_t elemtype;
    __global slot_t *elem_p;

    // Setup Output
    __global slot_t *dump_elements_p = get_object_pointer(output_p,0);
    //

    // Setup particle
    size_t partid = get_global_id(0);
    Particle particle;
    Particle *const particle_p=&particle;
    copy_particle_from(particles_p, partid, particle_p);

    // Track
    for (int iturn=0; iturn<nturns; iturn++){
        for (size_t ielem=0; ielem<nelems; ielem++){
            if (particle.islost>=0){
              // Element-by-element
              if (particle.turns<dump_element_nturns){
                  copy_particle_to(dump_elements_p,
                                   partid*nelems*dump_element_nturns+
                                   ielem*dump_element_nturns+
                                   particle.turns,
                                   particle_p);
              };// end element-by-element
              elemtype = element[ielem].type;
              elem_p = &elements_p[(element[ielem].address-elem_base)/8];
              switch (elemtype){
                case DriftID:
                  Drift_track((__global Drift *) elem_p, particle_p);
                  if (check_bounds(particle_p,1.0)) particle.islost=-ielem;
                  break;
                case DriftExactID:
                  DriftExact_track((__global Drift *) elem_p, particle_p);
                  if (check_bounds(particle_p,1.0)) particle.islost=-ielem;
                  break;
                case MultipoleID:
                  Multipole_track((__global Multipole *) elem_p, particle_p);
                  break;
                case CavityID:
                  Cavity_track((__global Cavity *) elem_p, particle_p);
                  break;
                case XYShiftID:
                  XYShift_track((__global XYShift *) elem_p, particle_p);
                  break;
                case SRotationID:
                  SRotation_track((__global SRotation *) elem_p, particle_p);
                  break;
#ifdef MONITOR_TRACK
                case MonitorID:
                  Monitor_track((__global Monitor *) elem_p,
                                particle_p,
                                output_p);
                  break;
#endif
              };
            } else {
                break;
            }; // end if not lost
        };//end for each element
        if (particle.islost>=0) {particle.turns++;}  else  break; ;
    };

    // Copy back
    copy_particle_to(particles_p, partid, particle_p);
};

