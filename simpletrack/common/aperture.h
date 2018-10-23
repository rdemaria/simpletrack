#ifndef ELEMENT_MEM
  #define ELEMENT_MEM
#endif


int check_bounds(Particle *p, double bound){
    if (X(p)> bound) return 1;
    if (X(p)<-bound) return 1;
    if (Y(p)> bound) return 1;
    if (Y(p)<-bound) return 1;
    return 0;
};

