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
    ELEMENT_INT(turns);
    ELEMENT_INT(start);
    ELEMENT_INT(skip);
    ELEMENT_INT(rolling);
    ELEMENT_INT(ref);
} Monitor;


void Monitor_track(ELEMENT_MEM Monitor *el,
                               PARTICLE(pp),
                               ELEMENT_MEM slot_t *output){
    ELEMENT_START
         TEMP_INT(const shifted) = (TURNS(pp)-el->start);
         if (shifted%el->skip==0 ){
            TEMP_INT(pos)= (shifted/el->skip);
            if (el->rolling==1) pos=pos%el->turns;
            if (pos >= 0 && pos < el->turns) {
              size_t partid = pos + PARTID(pp)*el->turns;
              ELEMENT_MEM slot_t *particles_p =
                                       get_object_pointer(output, el->ref);
              copy_particle_to(particles_p, partid, PARTICLE_SELF(pp));
            };
         };
    ELEMENT_STOP
};

