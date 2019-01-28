#ifndef MULTIPOLE_TRACK
  #define MULTIPOLE_TRACK
#endif



typedef struct {
    ELEMENT_INT(order) ;
    ELEMENT_REAL(length) ;
    ELEMENT_REAL(hxl) ;
    ELEMENT_REAL(hyl) ;
    ELEMENT_REAL(bal[1]);
} Multipole;

void Multipole_track(ELEMENT_MEM Multipole *el, PARTICLE(pp)){
    ELEMENT_REAL(ELEMENT_MEM *bal) = el->bal;
    ELEMENT_INT(const order) = el->order;
    ELEMENT_REAL(const length) = el->length;
    ELEMENT_REAL(const hxl) = el->hxl;
    ELEMENT_REAL(const hyl) = el->hyl;
    ELEMENT_START
        TEMP_REAL(const x) = X(pp);
        TEMP_REAL(const y) = Y(pp);
        TEMP_REAL(const chi) = CHI(pp);
        TEMP_REAL() dpx, dpy, zre, zim;

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
            TEMP_REAL(const b1l) = chi * bal[0];
            TEMP_REAL(const a1l) = chi * bal[1];
            TEMP_REAL(const hxx) = hxl / length * x;
            TEMP_REAL(const hyy) = hyl / length * y;
            TEMP_REAL(const delta) = DELTA(pp);
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
