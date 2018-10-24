#ifndef MONITOR_TRACK
  #define MONITOR_TRACK
#endif

#ifndef ELEMENT_MEM
  #define ELEMENT_MEM
#endif

#ifndef NAN
  #include <math.h>
#endif


typedef struct {
    INT(turns);
    INT(start);
    INT(skip);
    INT(rolling);
    INT(ref);
} Monitor;


void Monitor_track(ELEMENT_MEM Monitor *el,
                               Particle *pp,
                               ELEMENT_MEM slot_t *output){
    INT(const shifted) = (pp->turns-el->start);
    if (shifted%el->skip==0 ){
       INT(pos)= (shifted/el->skip);
       if (el->rolling==1) pos=pos%el->turns;
       if (pos >= 0 && pos < el->turns) {
         size_t partid = pos + pp->partid*el->turns;
         printf("pp %d\n",el->ref);
         ELEMENT_MEM slot_t *particles_p =
                                  get_object_pointer(output, el->ref);
         copy_particle_to(particles_p, partid, pp);
       };
    };
};

