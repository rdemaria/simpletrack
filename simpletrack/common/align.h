#ifndef XYSHIFT_TRACK
  #define XYSHIFT_TRACK
#endif

#ifndef SROTATION_TRACK
  #define SROTATION_TRACK
#endif


#ifndef ELEMENT_MEM
  #define ELEMENT_MEM
#endif

#ifndef M_PI
  #include <math.h>
#endif

typedef struct {
    ELEMENT_REAL(dx);
    ELEMENT_REAL(dy);
} XYShift;

void XYShift_track(ELEMENT_MEM XYShift *el, PARTICLE(pp)){
    ELEMENT_START
        X(pp)-=el->dx;
        Y(pp)-=el->dy;
    ELEMENT_STOP
};

typedef struct {
    ELEMENT_REAL(cos_z);
    ELEMENT_REAL(sin_z);
} SRotation;

void SRotation_track(ELEMENT_MEM SRotation *el, PARTICLE(pp) ){
    ELEMENT_START
         TEMP_REAL(const cos_z) = el->cos_z;
         TEMP_REAL(const sin_z) = el->sin_z;
         TEMP_REAL() x,y;
         x=X(pp); y=Y(pp);
         X(pp) = cos_z*x + sin_z*y;
         Y(pp) =-sin_z*x + cos_z*y;
         x=PX(pp); y=PY(pp);
         PX(pp) = cos_z*x + sin_z*y;
         PY(pp) =-sin_z*x + cos_z*y;
    ELEMENT_STOP
};

