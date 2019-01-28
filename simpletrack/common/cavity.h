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
    ELEMENT_REAL(voltage);
    ELEMENT_REAL(kfreq);
    ELEMENT_REAL(phase);
} Cavity;

void Cavity_track(ELEMENT_MEM Cavity *el, PARTICLE(pp) ){
    ELEMENT_START
         TEMP_REAL(const p0c) = P0C(pp);
         TEMP_REAL(const beta0) = BETA0(pp);
         TEMP_REAL(const charge0) = CHARGE0(pp);
         TEMP_REAL(const delta) = DELTA(pp);
         TEMP_REAL(const tau) = TAU(pp);
         TEMP_REAL(const chi) = CHI(pp);
         TEMP_REAL(const mass0) = MASS0(pp);

         TEMP_REAL(const phase) = el->phase - el->kfreq*tau;
         TEMP_REAL(const deltae) = (chi*charge0) * (el->voltage * sin(phase)) ;

         TEMP_REAL(const rep) = sqrt(delta*delta+2*delta+1/(beta0*beta0)) + deltae/p0c; //psigma + DeltaE/P0c
         TEMP_REAL(const ibg0) = mass0/p0c;
         TEMP_REAL(const irpp) = sqrt(rep*rep - ibg0*ibg0);
         RPP(pp)=1/irpp;
         DELTA(pp) = irpp-1;
         TEMP_REAL(const beta) = irpp/rep;
         RVV(pp) = beta/beta0;
         ZETA(pp) = tau*beta;
    ELEMENT_STOP
};


