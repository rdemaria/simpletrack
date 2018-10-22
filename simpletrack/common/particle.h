#ifndef COMMON_PARTICLE
#define COMMON_PARTICLE


/* python
import simpletrack as sim
sim.Particles._gen_common_particle_slots()
*/
#define PARTICLE_SLOTS  \
  REAL(x);              \
  REAL(px);             \
  REAL(y);              \
  REAL(py);             \
  REAL(zeta);           \
  REAL(delta);          \
  REAL(rpp);            \
  REAL(rvv);            \
  REAL(mass0);          \
  REAL(p0c);            \
  REAL(beta0);            \
  REAL(charge0);        \
  REAL(rmass);          \
  REAL(rcharge);        \
  REAL(chi);            \
  INT(turns);           \
  INT(islost);          \
/* end python */

/* python
import simpletrack as sim
sim.Particles._gen_common_particle_accessors()
*/
#define X(p)       PARTICLE_GET(p,x)
#define PX(p)      PARTICLE_GET(p,px)
#define Y(p)       PARTICLE_GET(p,y)
#define PY(p)      PARTICLE_GET(p,py)
#define ZETA(p)    PARTICLE_GET(p,zeta)
#define DELTA(p)   PARTICLE_GET(p,delta)
#define RPP(p)     PARTICLE_GET(p,rpp)
#define RVV(p)     PARTICLE_GET(p,rvv)
#define BETA0(p)   PARTICLE_GET(p,beta0)
#define MASS0(p)   PARTICLE_GET(p,mass0)
#define P0C(p)     PARTICLE_GET(p,p0c)
#define BETA0(p)   PARTICLE_GET(p,beta0)
#define CHARGE0(p) PARTICLE_GET(p,charge0)
#define RMASS(p)   PARTICLE_GET(p,rmass)
#define RCHARGE(p) PARTICLE_GET(p,rcharge)
#define CHI(p)     PARTICLE_GET(p,chi)
#define TURNS(p)   PARTICLE_GET(p,turns)
#define ISLOST(p)  PARTICLE_GET(p,islost)
/* end python */

#define XP(p)   (PX(p)*RPP(p))
#define YP(p)   (PY(p)*RPP(p))
#define BETA(p) (RVV(p)*BETA0(p))
#define TAU(p)  (ZETA(p)/BETA(p))
#define CHARGE(p) (RCHARGE(p)/CHARGE0(p))
#endif
