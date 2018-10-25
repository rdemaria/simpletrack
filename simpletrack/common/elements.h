#ifndef COMMON_ELEMENTS
#define COMMON_ELEMENTS

typedef enum type_t {
  DriftID = 2,
  DriftExactID = 3,
  MultipoleID = 4,
  CavityID = 5,
  XYShiftID = 6,
  SRotationID = 7,
#ifdef BEAMBEAM4D_TRACK
  BeamBeam4D = 8,
#endif
#ifdef BEAMBEAM6D_TRACK
  BeamBeam6D = 9,
#endif
#ifdef MONITOR_TRACK
  MonitorID = 10
#endif
} type_t;

#endif
