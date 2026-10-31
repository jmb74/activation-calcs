#!/usr/bin/env python3
"""Approximate v6 loading estimate, calibrated to v5 means; not FLUKA transport.

See analysis/target2_v6_setup.md for assumptions, sources and limitations.
"""
import math,json
A=math.pi; mc0=.4429;ms=.2+.2*70.9/226;mt=mc0+ms
Ein0=18.468347455170527;Eout0=13.248398615684497
slope=(18.654026463177313-Ein0)/.15
Ein=Ein0+slope*.05;target=Ein-(Ein0-Eout0+.7)
# Simplified Bethe electronic stopping in MeV cm2/g, neglecting corrections.
# Graphite I=81 eV (NIST ICRU90 summary); mixture I=150.44 eV and
# weighted Z/A=.46653 are printed in this FLUKA run's .out.
def stopping(E,za,I):
 M=938.27208816;me=.51099895;g=1+E/M;b2=1-1/g**2
 tmax=2*me*b2*g*g/(1+2*g*me/M+(me/M)**2)
 return .307075*za/b2*(.5*math.log(2*me*b2*g*g*tmax/(I*1e-6)**2)-b2)
def model(Ein,mc,scale):
 E=Ein;N=1200
 for _ in range(N):
  def f(x):
   C=stopping(x,6/12.0107,81)
   baseline=mt*stopping(x,.46653,150.44)
   return -scale*(baseline+(mc-mc0)*C)/A
  k=f(E);E+=f(E+.5*k/N)/N
 return E
a,b=.5,1.5
for _ in range(45):
 x=(a+b)/2
 if model(Ein0,mc0,x)>Eout0:a=x
 else:b=x
scale=(a+b)/2
a,b=mc0,.6
for _ in range(45):
 x=(a+b)/2
 if model(Ein,x,scale)>target:a=x
 else:b=x
mass=(a+b)/2
print(json.dumps(dict(entrance_est_MeV=Ein,target_exit_MeV=target,calibration_scale=scale,graphite_est_g=mass,rounded_trial_g=.51,rounded_trial_exit_est_MeV=model(Ein,.51,scale),density_for_051=(.51+ms)/(math.pi*.1)),indent=2))
