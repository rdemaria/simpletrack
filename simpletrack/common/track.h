// need definition of check_is_notlost, increase_turn, copy_particle_to_dump_element

void track_loop(PARTICLE(particle_p),
                ELEMENT_MEM slot_t *output_p,
                ELEMENT_MEM slot_t *elements_p,
                long nelems,
                long nturns,
                long dump_element_nturns ) {

    // Setup Elements
    ELEMENT_MEM Object *element = get_objects(elements_p);
    const size_t elem_base = get_base(elements_p);
    type_t elemtype;
    ELEMENT_MEM slot_t *elem_p;

    // Setup Output
    ELEMENT_MEM slot_t *dump_elements_p = get_object_pointer(output_p,0);

    // Track
    for (int iturn=0; iturn<nturns; iturn++){
    //for (; pp->turns<nturns;){
        for (size_t ielem=0; ielem<nelems; ielem++){
            if (check_is_notlost(particle_p)){
              // Element dump
              copy_particle_to_dump_element(
                          dump_elements_p, particle_p,
                          ielem, nelems, dump_element_nturns);
              // Element setup
              elemtype = element[ielem].type;
              elem_p = &elements_p[(element[ielem].address-elem_base)/8];
              // Jump table
              switch (elemtype){
                case DriftID:
                  Drift_track((ELEMENT_MEM Drift *) elem_p, particle_p);
                  check_bounds(particle_p,1.0,ielem);
                  break;
                case DriftExactID:
                  DriftExact_track((ELEMENT_MEM Drift *) elem_p, particle_p);
                  check_bounds(particle_p,1.0,ielem);
                  break;
                case MultipoleID:
                  Multipole_track((ELEMENT_MEM Multipole *) elem_p, particle_p);
                  break;
                case CavityID:
                  Cavity_track((ELEMENT_MEM Cavity *) elem_p, particle_p);
                  break;
                case XYShiftID:
                  XYShift_track((ELEMENT_MEM XYShift *) elem_p, particle_p);
                  break;
                case SRotationID:
                  SRotation_track((ELEMENT_MEM SRotation *) elem_p, particle_p);
                  break;
    #ifdef MONITOR_TRACK
                case MonitorID:
                  Monitor_track((ELEMENT_MEM Monitor *) elem_p,
                                particle_p,
                                output_p);
                  break;
    #endif
                  };
            } else {
                break;
            }; // end if not lost
        };//end for each element
        if (check_is_notlost(particle_p)) {
            increase_turn(particle_p);
        } else {
            break ;
        };
    };

};


