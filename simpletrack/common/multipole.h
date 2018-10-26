#ifndef MULTIPOLE_TRACK
  #define MULTIPOLE_TRACK
#endif



typedef struct {
    INT(order) ;
    REAL(length) ;
    REAL(hxl) ;
    REAL(hyl) ;
    REAL(bal[1]);
} Multipole;

void Multipole_track(ELEMENT_MEM Multipole *el, PARTICLE(pp)){
    REAL(ELEMENT_MEM *bal) = el->bal;
    INT(const order) = el->order;
    REAL(const length) = el->length;
    REAL(const hxl) = el->hxl;
    REAL(const hyl) = el->hyl;
    ELEMENT_START
        REAL(const x) = X(pp);
        REAL(const y) = Y(pp);
        REAL(const chi) = CHI(pp);
        REAL() dpx, dpy, zre, zim;

        dpx = bal[order * 2];
        dpy = bal[order * 2 + 1];
        for (int ii = order - 1; ii >= 0; ii--) {
          zre = (dpx * x - dpy * y);
          zim = (dpx * y + dpy * x);
          dpx = bal[ii * 2] + zre;
          dpy = bal[ii * 2 + 1] + zim;
        }
        dpx = -chi * dpx;
        dpy =  chi * dpy;
        if (length > 0) {
            REAL(const b1l) = chi * bal[0];
            REAL(const a1l) = chi * bal[1];
            REAL(const hxx) = hxl / length * x;
            REAL(const hyy) = hyl / length * y;
            REAL(const delta) = DELTA(pp);
            dpx += hxl;
            dpy -= hyl;
            dpx += hxl * delta - b1l * hxx;
            dpy -= hyl * delta - a1l * hyy;
            ZETA(pp) -= chi * (hxx - hyy) * length;
        };
        PX(pp)+=dpx;
        PY(pp)+=dpy;
    ELEMENT_STOP
};
