#ifndef COMMON_BUFFER
#define COMMON_BUFFER

typedef union {
      long i64;
      double f64;
} slot_t;

typedef struct {
  size_t base;
  size_t size;
  size_t size_header;
  size_t p_slots;
  size_t p_objects;
  size_t p_pointers;
  size_t p_garbage;
} Buffer;

typedef struct {
  size_t address;
  size_t type;
  size_t size;
} Object;

typedef struct {
  size_t size;
  size_t n_objects;
  Object objects[1];
} Objects;


size_t get_base(  ELEMENT_MEM slot_t *buffer) {
     ELEMENT_MEM Buffer *b = (ELEMENT_MEM Buffer *) buffer;
     return b->base;
}

size_t get_nobjects( ELEMENT_MEM slot_t *buffer) {
    ELEMENT_MEM Buffer *b = (ELEMENT_MEM Buffer *) buffer;
    return buffer[(b->p_objects - b->base)/8].i64;
};

ELEMENT_MEM Object *get_objects( ELEMENT_MEM slot_t *buffer) {
    ELEMENT_MEM Buffer *b = (ELEMENT_MEM Buffer *) buffer;
    return (ELEMENT_MEM Object *) &buffer[(b->p_objects - b->base)/8+2];
};

ELEMENT_MEM slot_t *get_object_pointer(ELEMENT_MEM slot_t *buffer,
                                     size_t object_pos) {
    size_t base = get_base(buffer);
    ELEMENT_MEM Object *objects = get_objects(buffer);
    return &buffer[(objects[object_pos].address-base)/8];
};


#endif

