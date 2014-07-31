# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 16:15:02 2014

@author: mstreet
"""

# Requirements:
# getIntGains should correctly generate the number of simulation hours from a
#             given start and stop date.
# getIntGains should explicitly not handle leap years.
# getIntGains should return a single vector of type numpy.ndarray that is the 
#             zone internal gain at each hour.
# getIntGains should be able to handle up to 14 different schedules (7 gain 
#             types with weekday or weekend schedule)
# getIntGains should not do the calculation for a general gain if the peak is
#             set to zero.
# getIntGains should not do the calculation for a distribution gain if either
#               the average heat or distribution length is zero.
# getIntGains should return a known solution for known inputs.


import unittest
import numpy as np
import annexCeqns as ISO
from classes import errorClassesSHM as EC
from simpleHourlyModel import genIntGains as gig
# import pdb


class GainsTestData(unittest.TestCase):
        def setUp(self):
            self.area = 10
            self.occDen = 10
            self.actLev = 100
            self.appDen = 10
            self.outAir = 10 # L/s/per
            self.lightDen = 10
            self.stop = (1,3,1) # stop 48 hours later
            self.wd_oc_sch = np.ones(24)
            self.we_oc_sch = np.ones(24)*0.5
            self.wd_app_sch = np.ones(24)
            self.we_app_sch = np.ones(24)*0.5
            self.wd_light_sch = np.ones(24)
            self.we_light_sch = np.ones(24)*0.5
            self.startDay = 6 # start on friday
            self.resGains = np.hstack([2400*3*np.ones(24), 
                                       1200*3*np.ones(24)])
            
        
class GainsTestKnownValues(GainsTestData):
    def test_KnownValuesGenIntGains(self):
        result = gig.genIntGains(A_floor = self.area,
                                 occDen = self.occDen,
                                 actLev = self.actLev,
                        oc_schd_wd = self.wd_oc_sch,
                        oc_schd_we = self.we_oc_sch,
                        appDen = self.appDen,
                        outAir = self.outAir,
                        app_schd_wd = self.wd_app_sch,
                        app_schd_we = self.we_app_sch,
                        lightDen = self.lightDen,
                        light_schd_wd = self.wd_light_sch,
                        light_schd_we = self.we_light_sch,
                        stop = self.stop, 
                        startDay = self.startDay)

        # Test that the function calculates the desired number of hours
        self.assertTrue(len(result) == 48)

        # Test that the result is the desired type
        self.assertTrue(isinstance(result, np.ndarray))
        
        # Test that the result equals a known value
        self.assertTrue(np.allclose(self.resGains, result))        
        
class GainsTestBadInput(GainsTestData):
    def test_BadInputGenIntGains(self):
        
        # Test that the funciton explicitly stops for any calculation
        # requesting a leap year        
        self.assertRaises(ValueError, gig.genIntGains,
                        A_floor = self.area, occDen = self.occDen,
                        actLev = self.actLev,
                        outAir = self.outAir,
                        oc_schd_wd = self.wd_oc_sch,
                        oc_schd_we = self.we_oc_sch,
                        appDen = self.appDen, 
                        app_schd_wd = self.wd_app_sch,
                        app_schd_we = self.we_app_sch,
                        lightDen = self.lightDen,
                        light_schd_wd = self.wd_light_sch, 
                        light_schd_we = self.we_light_sch,
                        stop = (2,29,12), startDay = self.startDay)
            
             
if __name__ == '__main__':
    unittest.main()