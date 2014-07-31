# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:26:22 2014

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
from simpleHourlyModel import getSolGains as gsg
# import pdb


class GainsTestData(unittest.TestCase):
        def setUp(self):
            # need to instantiate the building object
            
            # need to instantiate the site object
            self.jan2hrs = np.ndarray([1115.046088768250,
                                       1364.255427321500])
            
        
class GainsTestKnownValues(GainsTestData):
    def test_KnownValuesGenIntGains(self):
        result = gsg.genSolGains(self.building, self.site,
                                 start = (1,1,15), stop = (1,1,16))

        # Test that the function calculates the desired number of hours
        self.assertTrue(len(result) == 2)

        # Test that the result is the desired type
        self.assertTrue(isinstance(result, np.ndarray))
        
        # Test that the result equals a known value
        self.assertTrue(np.allclose(self.jan2hrs, result, atol = 1e-05))        
        
class GainsTestBadInput(GainsTestData):
    def test_BadInputGenIntGains(self):
        
        # Test that the funciton explicitly stops for any calculation
        # requesting a leap year        
        self.assertRaises(ValueError, gsg.genSolGains, self.building,
                          self.site, start = (2,28,22), stop = (2,29,15))
        
        # Test that the function fails for non dates
        self.assertRaises(ValueError, gsg.genSolGains, self.building,
                          self.site, start = (1,1,1), stop = (1,33, 3))
        
        # Test that the function fails for non hours
        self.assertRaises(ValueError, gsg.genSolGains, self.building, 
                          self.site, start = (1,1,0), stop = (1,1,15))
        
        self.assertRaises(ValueError, gsg.genSolGains, self.building, 
                          self.site, start = (1,1,1), stop = (1,1,35))
            
             
if __name__ == '__main__':
    unittest.main()