
#define REAL(name) double name
#define INT(name) long name
#define ELEMENT_MEM __global


size_t get_base(  __global slot_t *buffer) {
     __global Buffer *b = (__global Buffer *) buffer;
     return b->base;
}

size_t get_nobjects( __global slot_t *buffer) {
    __global Buffer *b = (__global Buffer *) buffer;
    return buffer[(b->p_objects - b->base)/8].i64;
};

__global Object *get_objects( __global slot_t *buffer) {
    __global Buffer *b = (__global Buffer *) buffer;
    return (__global Object *) &buffer[(b->p_objects - b->base)/8+2];
};

__global slot_t *get_object_pointer(__global slot_t *buffer,
                                     size_t object_pos) {
    size_t base = get_base(buffer);
    __global Object *objects = get_objects(buffer);
    return &buffer[(objects[object_pos].address-base)/8];
};
