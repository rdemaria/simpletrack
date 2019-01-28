#ifndef ELEMENT_MEM
  #define ELEMENT_MEM
#endif


void check_bounds(PARTICLE(pp), double bound, size_t ielem){
    ELEMENT_START
       if (!( (X(pp) < bound) && (X(pp) > - bound) &&
              (Y(pp) < bound) && (Y(pp) > - bound)   ) )
       {
           ISLOST(pp)=-ielem;
       }
    ELEMENT_STOP
};
