#include "common/elements.h"

#define REAL(name) double name
#define INT(name) long name
#define ELEMENT_MEM __global


__global Object* get_element_pointer( __global slot_t *elements_p);
size_t get_nelements( __global slot_t *elements_p);

__global Object * get_element_pointer( __global slot_t *elements_p) {
    __global Buffer *p = (__global Buffer *) elements_p;
    return (__global Object *) &elements_p[(p->p_objects - p->base)/8+2];
};

size_t get_nelements( __global slot_t *elements_p) {
    __global Buffer *p = (__global Buffer *) elements_p;
    return elements_p[(p->p_objects - p->base)/8].i64;
};

size_t get_base(  __global slot_t *elements_p) {
     __global Buffer *p = (__global Buffer *) elements_p;
     return p->base;
}

