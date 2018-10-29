
void track(slot_t *particle_p,
           slot_t *output_p,
           slot_t *elements_p,
           long nelems,
           long nturns,
           long dump_element_nturns ) {

    Particles particles;

    setup_particles(&particles,particle_p);

    track_loop(&particles,output_p,elements_p,nelems,nturns,dump_element_nturns);

};

