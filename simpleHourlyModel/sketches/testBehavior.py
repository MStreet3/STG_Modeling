# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 11:37:00 2014

@author: mstreet
"""
import numpy as np
import annexCeqns as ISO
import ISOsimpleHourlyModel as shm

A_fac = 4
A_flr = 1
U = 1
A_m = 2.5
C_m = 165000
A_win = 0
phi_int = 0
phi_sol = 1
v_flo = 0.01
A_roof = 1
theta_set_c = 20
theta_set_h = 15
theta_e = 25
theta_m_0 = 17
theta_sup = 25
phi_h_max = 10000
phi_c_max = -10000
phi_hc_need_10 = 10
deadBand = 2
theta_m_t_1 = 17
A_t = 4.5*A_flr
       
# Calculate transmission coefficients
H_is = ISO.calcH_is(A_flr)
H_vent = ISO.calcH_vent(v_flo)
H_ms = ISO.calcH_ms(A_m)        
H_op = (A_fac*U + A_flr*U +
        A_roof*U)
        
H_win = A_win*U
        
H_em = ISO.calcH_em(H_op,H_ms)
        
H_1 = ISO.calcH_1(H_vent, H_is)
H_2 = ISO.calcH_2(H_1, H_win)
H_3 = ISO.calcH_3(H_2, H_ms) 

# calculate heat flows annex C.2        
phi_ia = ISO.calcQ_ia(phi_int)
phi_m = ISO.calcQ_m(phi_int, phi_sol, A_m,
                         A_t)

phi_st = ISO.calcQ_st(phi_int, phi_sol,
                           A_m, A_t,H_win)

res = shm.calcBuildingDemand(phi_ia,
                       phi_m,
                       phi_st,
                       phi_h_max,
                       phi_c_max,
                       phi_hc_need_10,
                       theta_set_c,
                       theta_set_h,
                       deadBand,
                       theta_e,
                       theta_m_t_1,
                       theta_sup,
                       C_m,
                       H_1,
                       H_2,
                       H_3,
                       H_em,
                       H_is,
                       H_ms,
                       H_vent,
                       H_win)

print res