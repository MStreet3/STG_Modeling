# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 17:54:14 2014

@author: mstreet
"""
from classes import errorClassesSHM as EC
import numpy as np
import annexCeqns as ISO
#import pdb



def checkMode(theta_air_0, theta_set_c, theta_set_h, deadBand):

    cooling = theta_air_0 >= theta_set_c + deadBand

    heating = theta_air_0 <= theta_set_h - deadBand    

    if cooling:

        theta_air_set = theta_set_c

    elif heating:

        theta_air_set = theta_set_h

    return theta_air_set
    
def getAirTemperatures(phi_ia,
                       phi_m,
                       phi_st,
                       phi_h_max,
                       phi_c_max,
                       phi_hc_need,
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
                       H_win):
    temps = [theta_e, theta_m_t_1, theta_sup]
    for degCentigrade in temps:
        check = degCentigrade < 100 and degCentigrade > -100
        if not check:
            raise EC.TempOutOfBoundError('Error in calculating the temperature'+
            ' for the current timestep.  Temperature is out of range.')
    
    phi_m_tot = ISO.calcQ_mtot(Q_m = phi_m, Q_st = phi_st, Q_ia = phi_ia,
                               Q_d = phi_hc_need, H_em = H_em, H_win = H_win,
                               H_v = H_vent, H_1 = H_1, H_2 = H_2, H_3= H_3,
                               theta_e = theta_e, theta_airin = theta_sup)

    theta_m_t = ISO.calcTheta_mt(theta_mt_1 = theta_m_t_1, C_m = C_m,
                                 H_3 = H_3, H_em = H_em, Q_mtot = phi_m_tot)
    
    theta_m = ISO.calcTheta_m(theta_m_t, theta_m_t_1)
    
    theta_s = ISO.calcTheta_s(Q_st = phi_st, Q_ia = phi_ia, Q_d = phi_hc_need,
                              H_ms = H_ms, H_win = H_win, H_v = H_vent, 
                              H_1 = H_1, theta_e = theta_e,
                              theta_airin = theta_sup, theta_m = theta_m)
    
    theta_air = ISO.calcTheta_i(Q_ia = phi_ia, Q_d = phi_hc_need,
                                H_is = H_is, H_v = H_vent,
                                theta_s = theta_s, theta_airin = theta_sup)
    
    theta_op = ISO.calcTheta_op(theta_i = theta_air, theta_s = theta_s)
    
    result = np.array([phi_m_tot, theta_m_t, theta_m, theta_s, theta_air,
                       theta_op])
    return result

def calcBuildingDemand(
                       phi_ia,
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
                       H_win):
  
    # step 1
    phi_hc_need = 0 

    resStep1 = getAirTemperatures(phi_ia, phi_m, phi_st, phi_h_max, phi_c_max,
                       phi_hc_need, theta_e, theta_m_t_1, theta_sup, C_m, H_1,
                       H_2, H_3, H_em, H_is, H_ms, H_vent, H_win)

    theta_air_0 = resStep1[4]

    theta_m_t = resStep1[1]
    
    cond1 = resStep1[4] >= theta_set_h - deadBand 

    cond2 = resStep1[4] <= theta_set_c + deadBand
    #pdb.set_trace()
    if  cond1 and cond2:

        phi_hc_need_ac = phi_hc_need

        phi_hc_need_un = phi_hc_need

        theta_air_ac = resStep1[4]

        result = np.array([phi_hc_need_ac, theta_m_t, phi_hc_need_un,
                           theta_air_ac])
    else:
        #pdb.set_trace()

    # step 2 (if necessary)
        theta_air_set = checkMode(theta_air_0, theta_set_c, theta_set_h,
                                  deadBand)

        resStep2 = getAirTemperatures(phi_ia, phi_m, phi_st, phi_h_max, 
                       phi_c_max, phi_hc_need_10, theta_e, theta_m_t_1,
                       theta_sup, C_m, H_1, H_2, H_3, H_em, H_is,
                       H_ms, H_vent, H_win)

        theta_air_10 = resStep2[4]

        delT_set = (theta_air_set - theta_air_0)

        delT_10 = (theta_air_10 - theta_air_0)
        
        phi_hc_need_un = phi_hc_need_10*delT_set/delT_10

        # step 3    
        #pdb.set_trace()
        powCheck1 = phi_hc_need_un >= phi_c_max

        powCheck2 = phi_hc_need_un <= phi_h_max
        
        if powCheck1 and powCheck2:
            
            resStep3 = getAirTemperatures(phi_ia, phi_m, phi_st, phi_h_max, 
                       phi_c_max, phi_hc_need_un, theta_e, theta_m_t_1,
                       theta_sup, C_m, H_1, H_2, H_3, H_em, H_is,
                       H_ms, H_vent, H_win)

            theta_m_t = resStep3[1]

            phi_hc_need_ac = phi_hc_need_un

            theta_air_ac = theta_air_set

            result = np.array([phi_hc_need_ac, theta_m_t, phi_hc_need_un,
                               theta_air_ac])
        
        # step 4 (if necessary)
        else:
            #pdb.set_trace()

            if phi_hc_need_un < 0:

                phi_hc_need_max = phi_c_max

            elif phi_hc_need_un > 0:

                phi_hc_need_max = phi_h_max

            else:

                raise EC.ZoneResponseError('For some reason the un-restricted ' 
                 + 'heating/cooling need is zero, but we are in Step 4 of the '
                 + 'calculation.')
            
            resStep4 = getAirTemperatures(phi_ia, phi_m, phi_st, phi_h_max, 
                       phi_c_max, phi_hc_need_max, theta_e, theta_m_t_1,
                       theta_sup, C_m, H_1, H_2, H_3, H_em, H_is,
                       H_ms, H_vent, H_win)
            
            phi_hc_need_ac = phi_hc_need_max

            theta_m_t = resStep4[1]

            theta_air_ac = resStep4[4]

            result = np.array([phi_hc_need_ac, theta_m_t, phi_hc_need_un,
                               theta_air_ac])
    #pdb.set_trace()
    return result

def calcBuildingDemandWrap():
    # This is the wrapper to the calcBuildingDemand function.
    #     phi_ia,
#                       phi_m,
#                       phi_st,
#                       phi_h_max,
#                       phi_c_max,
#                       phi_hc_need_10,
#                       theta_set_c,
#                       theta_set_h,
#                       deadBand,
#                       theta_e,
#                       theta_m_t_1,
#                       theta_sup,
#                       C_m,
#                       H_1,
#                       H_2,
#                       H_3,
#                       H_em,
#                       H_is,
#                       H_ms,
#                       H_vent,
#                       H_win
    # This function calls the pre-functions required.  I guess these could all
    # be methods of the ISOBuilding class, but....
    
    # Which are time dependent inputs to calcBuildingDemand and which aren't?
    
    # What is the proper specification of the loop?
    # This function needs Qint and Qsol for each hour that calcBuildingDemand 
    # is to be calculated..
    
    # What are the inputs?
    
    pass
    