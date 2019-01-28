#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>


#include "cpu/elements.h"
#include "cpu/particles.h"

#include "common/buffer.h"
#include "common/aperture.h"
#include "common/drift.h"
#include "common/multipole.h"
#include "common/cavity.h"
#include "common/align.h"
#include "common/monitor.h"
#include "common/elements.h"
#include "common/track.h"


void track(Particles *particles_p,
           slot_t *output_p,
           slot_t *elements_p,
           long nelems,
           long nturns,
           long dump_element_nturns ) {

    if ( setup_particles(particles_p)!=-1 ){
        track_loop(particles_p,output_p,elements_p,
                nelems,nturns,dump_element_nturns);
    };
};

