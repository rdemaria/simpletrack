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

#endif

