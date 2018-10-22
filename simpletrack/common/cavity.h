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
    REAL(frequency);
    REAL(lag);
} Cavity;

void Cavity_track(ELEMENT_MEM Cavity *el, PARTICLE pp){
    REAL(const p0c) = P0C(pp);
    REAL(const beta0) = BETA0(pp);
    REAL(const charge0) = CHARGE0(pp);
    REAL(const delta) = DELTA(pp);
    REAL(const tau) = TAU(pp);
    REAL(const chi) = CHI(pp);

    REAL(const phase) = el->phase - el->kfreq*tau;
    REAL(const deltae) = (chi*charge0) * (el->voltage * sin(phase)) ;

    REAL(const rep) = sqrt(delta*delta+2*delta+1/(beta0*beta0)) + deltae/p0c;
    REAL(const bg0) = p0c/mass0;
    REAL(const rpp) = sqrt(rep*rep - bg0**2);
    RPP(pp)=rpp;
    DELTA(pp) = rpp-1;
    beta = rpp/rep;
    RVV(pp) = beta/beta0;
    ZETA(pp) = tau*beta;
};


