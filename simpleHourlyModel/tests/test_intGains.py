# -*- coding: utf-8 -*-
"""
Created on Wed Jul 09 14:45:11 2014

@author: mstreet
"""
# Requirements:
# calcPhi_oc  should take in either 24 or 1 values of the schedule fraction 
#             and return the heat gain in W for the hour.
# calcPhi_oc  should only receive at most one value for the other variables.
#             except in the case of the activity level, which can be specified
#             as 24 values.  In this case, these values should be multiplied
#             element wise by the schedule fraction. Else raise ScheduleError
# calcPhi_oc  should only return positive values (i.e., people may only act as
#             sources of thermal energy recovered in the zone.) Else raise 
#             ValueError.
# calcPhi_gen should meet same requirements as calcPhi_oc except raise 
#             ScheduleError if an input other than schedule fraction is 
#             specified with more than 1 value.
# calcPhi_genDis should meet all requirements of other heat functions.
# calcQ_int   If arguments not  the same length raise ScheduleError.  


import unittest
import numpy as np
import annexCeqns as ISO
from classes import errorClassesSHM as EC
# import pdb


class GainsTestData(unittest.TestCase):
        def setUp(self):
            self.dens = 1.
            self.area = 1.
            self.actLev = 200.
            self.SchFra = 0.75
            self.schFraLon = 0.75*np.ones(24)
            self.densLon = np.ones(24)*self.dens
        
class test_KnownValues(GainsTestData):
    
    """ 
    Each function should return known result for known values.   
    """

    def test_KnownPhi_oc(self):
        
        res = ISO.calcPhi_oc(self.dens, self.area, self.actLev, self.SchFra)
        self.assertTrue(np.allclose(res, 150.))
        
        resLong = ISO.calcPhi_oc(self.dens, self.area, 
                                 self.actLev, self.schFraLon)
        self.assertTrue(np.allclose(resLong, 150*np.ones(24)))
        
    
    def test_KnownPhi_gen(self):
        
        __ = [self.SchFra, self.schFraLon]
        ans = [.75, np.ones(24)*.75]
        for i in range(len(__)):
            res = ISO.calcPhi_gen(self.dens, self.area, __[i])
            res2 = ISO.calcPhi_genDis(self.dens, self.area, __[i])          
            cond  = np.allclose(res, ans[i])
            cond2 = np.allclose(res2, ans[i])
            self.assertTrue(cond and cond2)
    
    def test_calcQ_int(self):
        
        tmp = [self.dens, self.densLon]
        ans = [6.5, np.ones(24)*6.5]
        for i in range(len(tmp)):
            inp = tmp[i]
            out = ans[i]
            res = ISO.calcQ_int(inp, inp, inp, inp, inp, inp, inp)
            self.assertTrue(np.allclose(res, out))

class test_BadInput(GainsTestData):
    """
    Functions should fail for conditions specified in the requirements.
    
    """
    def test_Phi_oc_BadInput(self):
        # Test that vectors not allowed in first two args
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_oc, self.densLon,
                                                        self.dens,
                                                        self.dens,
                                                        self.dens)
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_oc,self.dens,
                                                        self.densLon,
                                                        self.dens,
                                                        self.dens)
        
#        Test that different sized last two args not allowed.                                                
#        self.assertRaises(EC.ScheduleError, ISO.calcPhi_oc,self.dens,
#                                                        self.dens,
#                                                        self.densLon,
#                                                        self.dens)
        # Test for no negative returns                                                
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_oc,self.dens,
                                                        self.dens,
                                                        -100.,
                                                        self.dens)
        # Test for element wise multiplication
        res =  ISO.calcPhi_oc(self.dens, self.dens, self.densLon,
                              self.densLon)                                                        
    
        self.assertTrue(np.allclose(res, self.densLon))
        
    def test_Phi_gen_BadInput(self):
        # Test that vectors not allowed in first two args
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_gen, self.densLon,
                                                        self.dens,
                                                        self.dens)
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_gen,self.dens,
                                                        self.densLon,
                                                        self.dens)
        
        # Test for no negative returns                                                
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_gen,self.dens,
                                                        self.dens,
                                                        -100)
        # Test for element wise multiplication
        res =  ISO.calcPhi_gen(self.dens, 0.5, self.densLon)                                                        
    
        self.assertTrue(np.allclose(res, 0.5*np.ones(len(self.densLon))))
        
    def test_Phi_genDis_BadInput(self):
        # Test that vectors not allowed in first two args
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_genDis, self.densLon,
                                                        self.dens,
                                                        self.dens)
        self.assertRaises(EC.ScheduleError, ISO.calcPhi_genDis,self.dens,
                                                        self.densLon,
                                                        self.dens)
        
        # negative returns possible if distribution pipes act as a room heat
        # sink.

        # Test for element wise multiplication
        res =  ISO.calcPhi_genDis(self.dens, self.dens, self.densLon)                                                        
    
        self.assertTrue(np.allclose(res, self.densLon))
    def test_Q_int_BadInput(self):
#        # Test that vectors all be same shape
        self.assertRaises(EC.ScheduleError, ISO.calcQ_int, self.densLon,
                                                        self.dens,
                                                        self.dens,
                                                        self.dens,
                                                        self.dens,
                                                        self.dens,
                                                        self.dens)
                                                              
             
if __name__ == '__main__':
    unittest.main()