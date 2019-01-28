#ifndef NAN
  #include <math.h>
#endif

#ifndef  DRIFT_TRACK
  #define DRIFT_TRACK
#endif


typedef struct {
    ELEMENT_REAL(length);
} Drift;

void Drift_track(ELEMENT_MEM Drift *el, PARTICLE(pp)){
    ELEMENT_REAL(const length) = el->length;
    ELEMENT_START
        TEMP_REAL(const xp) = PX(pp)*RPP(pp);
        TEMP_REAL(const yp) = PY(pp)*RPP(pp);
        X(pp)+= xp * length;
        Y(pp)+= yp * length;
        ZETA(pp) += length*(RVV(pp)-(1+(xp*xp+yp*yp)/2));
    ELEMENT_STOP
};

void DriftExact_track(ELEMENT_MEM Drift *el, PARTICLE(pp)){
    ELEMENT_REAL(const length) = el->length;
    ELEMENT_START
        TEMP_REAL(const opd) = 1 + DELTA(pp);
        TEMP_REAL(const px) = PX(pp);
        TEMP_REAL(const py) = PY(pp);
        TEMP_REAL(const lpzi) = length / sqrt(opd*opd- px*px- py*py);
        X(pp)+= px * length;
        Y(pp)+= py * length;
        ZETA(pp) += length*RVV(pp) - opd*lpzi;
    ELEMENT_STOP
};
