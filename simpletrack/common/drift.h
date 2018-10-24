#ifndef NAN
  #include <math.h>
#endif

#ifndef  DRIFT_TRACK
  #define DRIFT_TRACK
#endif


typedef struct {
    REAL(length);
} Drift;


void Drift_track(ELEMENT_MEM Drift *el, Particle *pp){
    REAL(const length) = el->length;
    REAL(const xp) = XP(pp);
    REAL(const yp) = YP(pp);
    X(pp)+= xp * length;
    Y(pp)+= yp * length;
    ZETA(pp) += length*(RVV(pp)-(1+(xp*xp+yp*yp)/2));
};

void DriftExact_track(ELEMENT_MEM Drift *el, Particle *pp){
    REAL(const length) = el->length;
    REAL(const opd) = 1 + DELTA(pp);
    REAL(const px) = PX(pp);
    REAL(const py) = PY(pp);
    REAL(const lpzi) = length / sqrt(opd*opd- px*px- py*py);
    X(pp)+= px * length;
    Y(pp)+= py * length;
    ZETA(pp) += length*RVV(pp) - opd*lpzi;
};

