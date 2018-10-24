#ifndef CAVITY_TRACK
  #define CAVITY_TRACK
#endif

#ifndef ELEMENT_MEM
  #define ELEMENT_MEM
#endif

#ifndef M_PI
  #include <math.h>
#endif

#define CLIGHT 299792458
#define M_2PI 2*M_PI


typedef struct {
    REAL(voltage);
    REAL(kfreq);
    REAL(phase);
} Cavity;

void Cavity_track(ELEMENT_MEM Cavity *el, PARTICLE pp){
    REAL(const p0c) = P0C(pp);
    REAL(const beta0) = BETA0(pp);
    REAL(const charge0) = CHARGE0(pp);
    REAL(const delta) = DELTA(pp);
    REAL(const tau) = TAU(pp);
    REAL(const chi) = CHI(pp);
    REAL(const mass0) = MASS0(pp);

    REAL(const phase) = el->phase - el->kfreq*tau;
    REAL(const deltae) = (chi*charge0) * (el->voltage * sin(phase)) ;

    REAL(const rep) = sqrt(delta*delta+2*delta+1/(beta0*beta0)) + deltae/p0c;
    REAL(const ibg0) = mass0/p0c;
    REAL(const irpp) = sqrt(rep*rep - ibg0*ibg0);
    RPP(pp)=1/irpp;
    DELTA(pp) = irpp-1;
    REAL(const beta) = irpp/rep;
    RVV(pp) = beta/beta0;
    ZETA(pp) = tau*beta;
};


