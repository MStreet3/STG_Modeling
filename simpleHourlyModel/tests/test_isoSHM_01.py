# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 10:39:13 2014

@author: mstreet
"""
# Requirements:
# calcBuildingDemand should return the heating or cooling need for given hour.
# calcBuildingDemand should only accept temperature values between -60 and 60
#                    °C.
# calcBuildingDemand should return a zero for no demand, negative value for
#                    a cooling demand, and a positive value for heating
#                    demand.  Units should be megajoules [MJ]
# calcBuildingDemand should return an array with four values: actual need, 
#                    instantaneous temperature at current timestep (theta_m_t),
#                    the unrestricted need, and the calculated air temperature.
# calcBuildingDemand should calculate the theta_m per eqn. C.4 of ISO 
#                    13790-2008 for each hour and store the value.

import unittest
import numpy as np
import ISOsimpleHourlyModel as isoSHM
import annexCeqns as ISO
import pdb

class ISOsimpleHourlyTestSuite(unittest.TestCase):
    """ 
    There are five operational modes that the function must be able to
    identify and correctly solve.  This base class defines the inputs and
    correct outputs for a fictional hour.  These results were manually 
    calculated in the excel file 'testcaseSHMbook'.
    
    """    
    def setUp(self):
        
        # Define building variables            
        self.A_facade = np.array([4.0, 4.0, 4.0, 4.0, 4.0]) # [m2]
        self.A_floor = np.array([1.0, 1.0, 1.0, 1.0, 1.0]) # [m2]
        self.A_roof = np.array([1.0, 1.0, 1.0, 1.0, 1.0]) # [m2]
        self.A_win = np.array([0.0, 0.0, 0.0, 0.0, 0.0]) # [m2]
        self.U_facade = np.ones(5) # [W/m2K]        
        self.U_floor = np.ones(5) # [W/m2K]
        self.U_roof = np.ones(5) # [W/m2K]
        self.U_win = np.ones(5) # [W/m2K]
        self.v_flo = np.array([1, 0.01, 0.01, 1.0, 1.0]) # [m3/s]
        self.classNum = 3*np.ones(5)
        self.phi_int = np.array([0.0, 0.0, 0.0, 0.0, 0.0]) # [w]
        self.phi_sol = np.array([1.0, 1.0, 1.0, 1.0, 1.0]) # [w]
        self.theta_set_c = 20*np.ones(5) # [C]
        self.theta_set_h = 15*np.ones(5) # [C]
        self.deadBand = 2*np.ones(5) 
        self.phi_h_max = 10000.0 # [W]
        self.phi_c_max = -10000.0 # [W]
        self.phi_need_10 = 10.0 # 10*floor area
        

        # Calculate Misc. variables
        self.A_t = 4.5*self.A_floor
        self.A_m = np.ones(len(self.A_floor))
        self.C_m = np.ones(len(self.A_floor))        
        __ = zip(self.A_floor, self.classNum)
        i = 0
        for area, cNum in __:
            self.A_m[i] = ISO.calcA_m(area, cNum)
            self.C_m[i] = ISO.calcC_m(area, cNum)
            i += 1
                
                # ignoring slab variables
        
        # Calculate transmission coefficients
        self.H_is = ISO.calcH_is(self.A_floor)
        self.H_vent = ISO.calcH_vent(self.v_flo)
        self.H_ms = ISO.calcH_ms(self.A_m)        
        
        self.H_op = (self.A_facade*self.U_facade + self.A_floor*self.U_floor +
        self.A_roof*self.U_roof)
        
        self.H_win = self.A_win*self.U_win
        
        self.H_em = ISO.calcH_em(self.H_op, self.H_ms)
        
        self.H_1 = ISO.calcH_1(self.H_vent, self.H_is)
        self.H_2 = ISO.calcH_2(self.H_1, self.H_win)
        self.H_3 = ISO.calcH_3(self.H_2, self.H_ms) 
        
        # calculate heat flows annex C.2        
        self.phi_ia = ISO.calcQ_ia(self.phi_int)
        self.phi_m = ISO.calcQ_m(self.phi_int, self.phi_sol, self.A_m,
                                 self.A_t)
        
        self.phi_st = ISO.calcQ_st(self.phi_int, self.phi_sol,
                                   self.A_m, self.A_t, self.H_win)
       
        # temperature conditions for the hour       
        self.theta_e = np.array([0, 13, 25, 25, 30]) # [C]
        self.theta_m_t_1 = np.array([5, 11, 17, 17, 27]) # [C]
        self.theta_sup = np.array([0,  13, 25, 25, 30]) # [C]
        
        
         # Known answers  
        self.phi_HC_nd_ac = np.array([self.phi_h_max,
                                 56.158672472988,
                                 0.0,
                                 -5980.425989875840,
                                 self.phi_c_max])# None value for now
        self.phi_HC_nd_un = np.array([18087.667428380400,
                                 56.158672472988,
                                 0.0,
                                 -5980.425989875840,
                                 -12061.4467794962])# [W]
        self.theta_m_t = np.array([4.8274698685755100,
                              11.9909677682371,
                              19.0531508926928,
                              18.7185242520848,
                              26.5674084389284])# [C]
        self.theta_air = np.array([8.307386965,
                                   15.0,
                                   21.9771214,
                                   20.0,
                                   21.7058646])
                              

class SingleZoneModelKnownOutput(ISOsimpleHourlyTestSuite):

    def test_calcBuildingDemandKnownOutput(self):
        """ 
        calcBuildingDemand should give known cooling demand for known value.
        """       
        for index in range(5):
            #pdb.set_trace()
            result = isoSHM.calcBuildingDemand(                                      
                                        self.phi_ia[index],
                                        self.phi_m[index],
                                        self.phi_st[index],
                                        self.phi_h_max,
                                        self.phi_c_max,
                                        self.phi_need_10,
                                        self.theta_set_c[index],
                                        self.theta_set_h[index],
                                        self.deadBand[index],
                                        self.theta_e[index],
                                        self.theta_m_t_1[index],
                                        self.theta_sup[index],
                                        self.C_m[index],
                                        self.H_1[index],
                                        self.H_2[index],
                                        self.H_3[index],
                                        self.H_em[index],
                                        self.H_is[index],
                                        self.H_ms[index],
                                        self.H_vent[index],
                                        self.H_win[index])
                                        
            cond0 = np.allclose(result[0], self.phi_HC_nd_ac[index],
                                atol = 1e-05)
            cond1 = np.allclose(result[1], self.theta_m_t[index],
                                atol = 1e-05)                            
            cond2 = np.allclose(result[2], self.phi_HC_nd_un[index],
                                atol = 1e-05)
            cond3 = np.allclose(result[3], self.theta_air[index],
                                atol = 1e-05)
            self.assertTrue(cond0 and cond1 and cond2 and cond3)

class SingleZoneModelBadInput(ISOsimpleHourlyTestSuite):
    def test_OutOfBoundTemp(self):
        """ 
        calcBuildingDemand should fail if the time step temperature is 
        out of bounds.
        """
        index = 0
        self.assertRaises(isoSHM.TempOutOfBoundError,
                          isoSHM.calcBuildingDemand,                        
                          self.phi_int[index],
                          self.phi_sol[index],
                          self.phi_st[index],
                          self.phi_h_max,
                          self.phi_c_max,
                          self.phi_need_10,
                          self.theta_set_c[index],
                          self.theta_set_h[index],
                          self.deadBand[index],
                          self.theta_e[index],
                          -100,
                          self.theta_sup[index],
                          self.C_m[index],
                          self.H_1[index],
                          self.H_2[index],
                          self.H_3[index],
                          self.H_em[index],
                          self.H_is[index],
                          self.H_ms[index],
                          self.H_vent[index],
                          self.H_win[index])
    

#if __name__ == '__main__':
#    unittest.main()

suite1 = unittest.TestLoader().loadTestsFromTestCase(SingleZoneModelKnownOutput)
suite2 = unittest.TestLoader().loadTestsFromTestCase(SingleZoneModelBadInput)     
alltests = unittest.TestSuite([suite1, suite2])
unittest.TextTestRunner(verbosity = 2).run(alltests)