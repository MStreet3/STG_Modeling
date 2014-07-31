# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:46:19 2014

@author: mstreet
"""
import math
import numpy as np
from classes import errorClassesSHM as EC
import pdb
""" Transmission Coefficients Calculations """

def calcH_is(A_fl):
    """
    Input:
    A_fl - seful floor area in m2 per section 6.3.2 of the standard
    
    Output:
    H_is - Coupling conductance eqn. 8 section 7.2.3.2 [W/K]

    """
    h_is = 3.45 # heat transfer between nodes i & s [W/m2K]    
    R_at = 4.5  # dimensionless ratio between internal surface area 
                # and floor area   
    A_tot = R_at * A_fl # m2
    H_is = h_is*A_tot
    return H_is

def calcH_em(H_op, H_ms):
    """
    Calculation of split based on §12.2.2 from 13790-2008
    
    Input:
    H_op - thermal transmission coeff. of opaque building elements 
    H_ms - coupling conductance between nodes m & s in [W/K]
    
    Output:
    H_em - transmission coeff. between exterior and ambient [W/K]
    """
    hp = 1.0/H_op
    hms = 1.0/H_ms
    H_em = 1.0/(hp - hms)
    return H_em
    
def calcH_tr_i(A_i, U_i):
    """
    This function calculates the resistance of a single building element
    based on the area and specified u-value.  The same equation is used for
    both opaque and non-opaque surfaces.  To get the total H_tr the elements
    must be summed together.  This function assumes no linear bridging 
    elements and no spot elements.
    
    EN ISO 13789-2008 § 4.3
    
    The transmission heat transfer coefficient through the building elements
    separating the conditioned space and the external air is calculated either
    directly by numerical methods according to ISO 10211 or according to
    Equation (2):
        
        H_D = sum_i^{n}{A_i*U_i} + sum_k^{n}{l_k*\psi_k} + 
              sum_j^{n}{\chi_j}
    
    Input:
    
    A_i - area of element i [m2]
    U_i - Uvalue of element i [W/m2K]
    
    Output:
    H_op - opaque element heat transfer coefficient [W/K]    
    
    """
    
    H_tr_i = A_i*U_i
    return H_tr_i   

def calcH_g(A_e, U_g, P_e, Psi_e = 0.60):

    """
    This function calculates the transmission heat transfer coefficient from 
    a building to the ground.  It assumes no linear bridging elements, but 
    accounts for perimeter losses.
    
    EN ISO 1370-2007 § 4
    
    d) The area related heat transfer calculated by the formulae given in
    this standard (see Clause 9), together with the edge-related coefficients
    obtained from, for example, tables prepared with ISO 14683.
        
        H_g = A*U + P*Psi
    
    Input:
    
    A_e - external area of ground floor [m2]
    U_g - Uvalue of ground floor [W/m2K]
    P_e - total external perimeter of ground floor [m] 
    Psi_e - linear transmisttance from ISO 14683 [W/mK]
    
    Default Psi value from Table A.2 of 14683-2007 GF2.
    
    Output:die Fläche des Bauteils j, angegeben in Quadratmeter.
    H_g - ground heat transfer coefficient [W/K]    
    
    """
    
    H_g = A_e*U_g + P_e*Psi_e
    return H_g
    
def calcV_flo(vol, ACH):
    """
    Calculate the volume flow rate in m3/s given the total ventilated
    volume and the specified air changes per hour.
    
    Input:
    vol - the volume of air to exchange in one hour.
    ACH - the specified number of air changes per hour.
    
    Output:
    v_flo - volume flow rate to achieve the specified ACH in m3/s
    
    """
    v_flo = ACH*vol/3600.0
    return v_flo
    
def calcH_vent(V_flo):

    """
    Input:
    V_flo - volume flow rate of entering air [m3/s]
    
    Output:
    H_v - heat transfer coefficient of ventilation transfer [W/K]
    per section 9.3.1 ISO 13790-2005
    """
    # 1200 J/m3K (rho_air*specificHeat_air)   
    H_v = 1200*V_flo
    return H_v
   
def calcH_ms(A_m):
    """
    Input:
    A_m - effective mass area from 12.2.2 [m2]
    
    Output:
    H_ms - coupling conductance between nodes m & s in [W/K]
    """
    h_ms = 9.1 # heat transfer coeff. given in 7.2.3.2 [W/m2K]
    H_ms = h_ms*A_m
    return H_ms  

def calcH_1(H_v, H_is):
    hv = 1.0/H_v
    his = 1.0/H_is
    H_1 = 1.0/(hv + his)
    return H_1
    
def calcH_2(H_1, H_win):
    H_2 = H_1 + H_win
    return H_2
    
def calcH_3(H_2, H_ms):
    h2 = 1.0/H_2
    hms = 1.0/H_ms
    H_3 = 1.0/(h2 + hms)
    return H_3

""" Temperature calculations """
    
def calcTheta_m(theta_mt, theta_mt_1):
    theta_m = 0.5*(theta_mt + theta_mt_1)
    return theta_m

def calcTheta_mt(theta_mt_1, C_m, H_3, H_em,
                 Q_mtot):
    c = C_m/3600.00
    h = H_3 + H_em
    a = theta_mt_1*(c - 0.5*h) + Q_mtot
    b = c + 0.5*h
    theta_mt = a/b
    return theta_mt

def calcTheta_s(Q_st, Q_ia, Q_d,
                H_ms, H_win, H_v, H_1,
                theta_e, theta_airin, theta_m):
                    
    b = H_ms + H_win + H_1

    q = Q_ia + Q_d

    c = theta_airin + q/H_v

    a = H_ms*theta_m + Q_st + H_win*theta_e + H_1*c

    theta_s = a/b
    
    return theta_s

def calcTheta_i(Q_ia, Q_d,
                H_is, H_v,
                theta_s, theta_airin):
    a = H_is*theta_s + H_v*theta_airin + Q_ia + Q_d
    b = H_is + H_v
    theta_i = a/b
    return theta_i
    
def calcTheta_op(theta_i, theta_s):
    theta_op = 0.3*theta_i + 0.7*theta_s
    return theta_op

""" Power Calculations """

def calcQ_ia(Q_int):
    Q_ia = 0.5*Q_int
    return Q_ia

def calcQ_m(Q_int, Q_sol, A_m, A_t):    
    Q_m = (A_m/A_t)*(0.5*Q_int + Q_sol)
    return Q_m
    
def calcQ_st(Q_int, Q_sol, A_m, A_t, H_es):
    a = A_m/A_t
    b = H_es/(9.1*A_t)
    Q_st = (1 - a - b)*(0.5*Q_int + Q_sol)
    return Q_st

def calcQ_mtot(Q_m, Q_st, Q_ia, Q_d,
               H_em, H_win, H_v, H_1, H_2, H_3,
               theta_e, theta_airin):
    q = Q_ia + Q_d # [W]
    a = (Q_st + H_win*theta_e + H_1*(q/H_v + theta_airin))
    Q_mtot = Q_m + H_em*theta_e + H_3*a/H_2
    return Q_mtot

def calcQ_int(phi_oc, phi_app, phi_light, phi_wa, phi_hvac, phi_proc,
              phi_adj, adjFac = 0.5):
    """
    
    Summation of heat sources for the hour.  Per equation 35 of ISO 13790-2008.
    Gains are positive.  Sinks are negative.
    
    Inputs: 
    phi_oc - occupant heat gain [W]
    phi_app - appliance heat gain [W]
    phi_light - lighting heat gain [W]
    phi_wa - water mains and sewage heat gains [W]
    phi_hvac - distribution gains or sinks from HVAC [W]
    phi_proc - gains from processes in the space [W]
    adjFac - adjustment factor for gains from unconditioned adjacent spaces.
             Find actual value from ISO 15193
    phi_adj - heat gained from an adjacent unconditioned Space [W]
    
    Outputs:
    
    Qint - internal heat gain of the thermal zone for the hour of 
           calculation. [W]
    
    """
    phi_args = [phi_oc, phi_app, phi_light, 
                phi_wa, phi_hvac, phi_proc, phi_adj]
    
    check1 = np.all(map(isinstance, phi_args, 
                        [float for i in range(len(phi_args))]))
    check2 = np.all(map(isinstance, phi_args, 
                        [np.ndarray for i in range(len(phi_args))]))
    if not check1 and not check2:
        raise EC.ScheduleError('Internal gain arguments must be of same type.'
        + '  Either all float or all numpy ndarray.')
    
    if check2:
        check3 = np.all(map(np.shape,
                            phi_args))
        if not check3:
            raise EC.SchuedleError('Internal gain arguments must be the same'
            + ' shape.')
    
    Qint = phi_oc + phi_app + phi_light + phi_wa + phi_hvac + phi_proc\
    + (1-adjFac)*phi_adj
    
    return Qint

def calcPhi_oc(occDen, area, actLev, schFra):
    """
    Calculate the average power contribution from zone occupants for the 
    given time step.  Neglects split into convective and radiative portions
    per the ISO 13790-2008 method.
    
    Input
    occDen - peak occupant density [people/m2]
    area - zone conditioned floor area [m2]
    actLev - activity level of occupants at time step [W/person]
    schFra - fraction of peak occupancy []
    
    Output
    phi_oc - average power contribution to the zone by occupants for the
            time step. The element-wise multiplication of all args.
    """        
    cond1 = isinstance(occDen, float)
    cond2 = isinstance(area, float)
    
    if not cond1 or not cond2:
        raise EC.ScheduleError('Occupant density and area must be ' +
               'single values.')

                  
    phi_oc = occDen*area*actLev*schFra

    cond5 = np.all(phi_oc >= 0)
    
    if not cond5:
        raise EC.ScheduleError('Occ. Gains should be positive.  Check inputs.')
    
    return phi_oc

def calcPhi_gen(peaDen, area, schFra):
    """
    Calculate the average power contribution from zone a general zone source
    given time step.  Neglects split into convective and radiative portions
    per the ISO 13790-2008 method.
    
    Useful function for lighting, appliances, process, and other loads needed
    to calculate Qint.
    
    Input
    appDen - peak power density [W/m2]
    area - zone conditioned floor area [m2]
    schFra - fraction of peak appliance use []
    
    Output
    phi_gen - average power contribution to the zone by a generalized source.
    """
    cond1 = isinstance(peaDen, float)
    cond2 = isinstance(area, float)
    
    if not cond1 or not cond2:
        raise EC.ScheduleError('Peak internal gain value and area must be ' +
               'single values.')
    
    phi_gen = peaDen*area*schFra
    cond3 = np.all(phi_gen >= 0)
    if not cond3:
        raise EC.ScheduleError('Gains should be positive.  Check inputs.')
    
    return phi_gen

def calcPhi_genDis(qAvg, lenDis, schFra):
    """
    Calculate the average power contribution to zone from the circulating pipe.
    Neglects split into convective and radiative portions per the
    ISO 13790-2008 method.   In general different lengths for supply
    and return with separate heat disappated or removed.  
    
    General calculation method for recoverable heat from either phi_wa or 
    phi_hvac.    
    
    Input
    qAvg - time averaged power dissapated from mains and pipes.  Recoverable
    heat only. [W/m]
    
    lenDis - length of circulating pipe.[m]
    
    Output
    phi_gen - average power contribution (or removal) from the zone by
    hot water and sewage distribution.
    """
    cond1 = isinstance(qAvg, float)
    cond2 = isinstance(lenDis, float)
    
    if not cond1 or not cond2:
        raise EC.ScheduleError('Average heat loss or gain by distribution ' +
               'and pipe length must be single values.')

    phi_genDis = qAvg*lenDis*schFra
    
    return phi_genDis   
    
def caclPhi_sol_k(shdFac, effArea, solIrr, skyFac, phi_sky):
    """
    Equation 43 of ISO 13790-2008
    
    Calculates the contribution of solar for each building element.
    
    Total contribution to solar is the sum of phi_sol_k for each building
    element.
    
    Input
    shdFac - shading reduction factor of building element k []
    effArea - effective area of building element per eqn. 44 or 45 [m2]
    solIrr - irradiation incident of building element based on tilt and azi
             [w/m2]
    skyFac - Building element to sky view factor []
    phi_sky - average power from building element to sky  [W]
    
    Output
    phi_sol_k - average power gain or loss for building element k. [w]
    
    """
    
    phi_sol_k = shdFac*effArea*solIrr - skyFac*phi_sky
    
    return phi_sol_k

def calcPhi_long(extRes, uVal, proAre, emiLon, locId = 2):
    """
    Average power gain or loss due to long wave radiation exchange with the
    sky.  External radiative heat transfer coefficient approximated as 
    five times the surface thermal emissivity.  Temperature difference assumed
    based on the approximate location of building.
    
    Assumptions per section 11.4.6 of ISO 13790-2008.
    
    Input
    extRes - external surface resistance of building element [m2K/W]
    uVal - thermal resistance of building element [W/m2K]
    proAre - project area of building envelope element [m2]
    emiLon - longwave, thermal emissivity of building element
    locId - identifier for selecting the temperature difference. 
            1 (sub-polar) - delTheta = 9 K
            2 (intermediate) - delTheta = 11 K
            3 (tropical) - delTheta = 13 K
    
    Output
    phi_long - longwave radiation average over the hour for element k. [W]
    """
    if proAre <= 0:
        raise ValueError('Object area must be a value greater than zero.')
    if locId in range(1,4):
        if locId == 1:
            delTheta = 9
        elif locId == 2:
            delTheta = 11
        elif locId == 3:
            delTheta = 13
    else:
        raise ValueError('Valid location ID' + "'" + 's are: 1 - sub-polar, ' 
                         + '2 - intermediate, ' + '3 - tropic.')
    h_rad = 5*emiLon
    phi_long = extRes*uVal*proAre*h_rad*delTheta
    
    return phi_long    

""" Misc. Variables """

def calcA_m(A_f, classNum):
    """
    Class specification per the DIN EN ISO 19790-2008 Table 12
    
    Input:
    A_f - conditioned floor area [m2]
    classNum - integer from 1 to 5 corresponding to construction type.
    
    Output:
    A_m - effective mass area of the building [m2]
    
    """
    if A_f <= 0:
        raise ValueError('Facade area must be a value greater than zero.')
    if classNum in np.array(range(5))+1:
        if classNum == 1:
            A_m = 2.5*A_f
        elif classNum == 2:
            A_m = 2.5*A_f
        elif classNum == 3:
            A_m = 2.5*A_f
        elif classNum == 4:
            A_m = 3.0*A_f
        else:
            A_m = 3.5*A_f
    else:
        raise ValueError('Valid building classes are: 1 - Very Light, ' 
                         + '2 - Light, ' + '3 - Medium, '+ '4 - Heavy, ' +
                         '5 - Very Heavy. ')
    return A_m

def calcC_m(A_f, classNum):
    """
    Class specification per the DIN EN ISO 19790-2008 Table 12
    
    Input:
    A_f - conditioned floor area [m2]
    classNum - integer from 1 to 5 corresponding to construction type.
    
    Output:
    C_m - effective mass of the building [J/K]
    
    """
    if A_f <= 0:
        raise ValueError('Facade area must be a value greater than zero.')
    
    if classNum in np.array(range(5))+1:
        if classNum == 1:
            C_m = 80000.0*A_f
        elif classNum == 2:
            C_m = 110000.0*A_f
        elif classNum == 3:
            C_m = 165000.0*A_f
        elif classNum == 4:
            C_m = 260000.0*A_f
        else:
            C_m = 370000.0*A_f
    else:
        raise ValueError('Valid building classes are: 1 - Very Light, ' 
                         + '2 - Light, ' + '3 - Medium, '+ '4 - Heavy, ' +
                         '5 - Very Heavy. ')
    return C_m

def calcU_g(dt, B_prime, lambda_s = 2.0):

    """
    Calculate the ground conductance based on the characteristic and
    equivalent thickness.
    
    Input:
    dt - the equivalent thickness [m]
    
    B_prime - characteristic length of ground floor [m]
    
    lambda_s - soil linear transmittance with default value from ISO 
    13370-2007 [W/mK]
    
    Output:
    U_g - overall ground floor conductance to be used in calculating the 
    ground heat transfer coefficient.
    """
    chkArg1 = dt > 0
    chkArg2 = B_prime > 0
    chkArg3 = lambda_s > 0
    
    if chkArg1 and chkArg2 and chkArg3:
        if dt < B_prime:
            arg = math.pi*B_prime/dt + 1.0
            num = 2.0*lambda_s
            den = math.pi*B_prime + dt        
            U_g = (num/den)*math.log(arg)
        else:
            U_g = lambda_s/(0.457*B_prime + dt)
      
    else:
        raise ValueError('All input arguments must be greater than zero.')
    
    return U_g

def calcB_prime(A_e, P_e):
    
    """
    Calculate the characteristic length of the ground floor.
    
    Input:
    A_e - external floor area of the ground floor. [m2]
    
    P_e - external perimeter of the ground floor. [m]
    
    Output:
    B_prime - chracteristic dimension of the ground floor [m]
    
    """
    checkArg1 = A_e > 0
    checkArg2 = P_e > 0
    if checkArg1 and checkArg2:
        B_prime = A_e/(0.5*P_e)
    else:
        raise ValueError('Both input arguments must be greater than zero.')
    return B_prime

def calcDt(w, R_si, R_f, R_se, lambda_s = 2.0):
    """
    Total equivalent thickness per ISO 13370-2007
    
    Input:
    w - the full thickness of the walls, including all layers [m]

    R_f - thermal resistance of the floor slab, including all-over insulation
    layers above, below, or within the floor slab, and that of any floor 
    covering.
    
    R_si - thermal resistance of internal surface [m2K/w]

    R_se - thermal resistance of external surface [m2K/W]
    
    Output:
    dt - total equivalent thickness [m]
    """
    chkArg1 = w > 0
    chkArg2 = R_si > 0
    chkArg3 = R_f > 0
    chkArg4 = R_se > 0
    chkArg5 = lambda_s > 0
    if chkArg1 and chkArg2 and chkArg3 and chkArg4 and chkArg5:
        dt = w + lambda_s*(R_si + R_f + R_se)
    else:
        raise ValueError('All arguments must have nominal values '+
        'greater than zero.')
    return dt

def calcA_eff_gl(movShd, gGl, frmFra, proAre):
    """
    The effective solar collecting area of a glazed envelope element. [m2]
    
    Input
    movShd - shading reduction factor for moveable shading provisions
             determined via 11.4.3 of standard.
    gGl - total solar energy transmittance of the transparent portion of the
          element determined according to 11.4.2 of standard
    frmFra - frame area fraction, ratio of projected frame area to the overall
             projected area of glazed element.
    proAre - overall projected area of the glazed element [m2]
    
    Output
    A_eff_gl - effective area of glazed area for use in calculating phi_sol_k.
    """
    A_eff_gl = movShd*gGl*(1-frmFra)*proAre
    
    return A_eff_gl

def calcA_eff_op(absOpa, extRes, uVal, proAre):
    """
    Calculates the effective solar collecting area of an opaque element of 
    the building envelope. [m2]
    
    Input
    absOpa - absorption coefficient for solar radiation.
    extRes - external surface resistance of the opaque element [m2K/w]
    uVal - thermal resistance of the opaque element [W/m2K]
    proAre - projected area of the opaque envelope element [m2]
    
    Output
    A_eff_op - effective solar collecting area of opaque element k. [m2]
    """
    
    A_eff_op = absOpa*extRes*uVal*proAre
    
    return A_eff_op