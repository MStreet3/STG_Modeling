# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:39:54 2014

@author: mstreet
"""

# Requirements
# genSchd should take in an integer representing the day of the first hour of
#         the weather file.  
# genSchd should return an np.array indicating the order of the week.
# genSchd should raise a ValueError if the input is outside of the range 1 to
#         7.
import unittest
import numpy as np
from simpleHourlyModel import helpFncs as hF

 
class GenSchdTestSetUp(unittest.TestCase):
    """
    Define some common set up procedures.
    
    """
    
    def setUp(self):
        pass
        
class genSchdKnownValues(GenSchdTestSetUp):
    """
    Function gives known values for known input.
    
    """
    def test_KnownInputGenSchd(self):    
        __ = [1,2,3,4,5,6,7]
        correct = np.array([[1,2,3,4,5,6,7],
                           [2,3,4,5,6,7,1],
                           [3,4,5,6,7,1,2],
                           [4,5,6,7,1,2,3],
                           [5,6,7,1,2,3,4],
                           [6,7,1,2,3,4,5],
                           [7,1,2,3,4,5,6]])

        for i in range(len(__)):
            
            output = hF.genSchd(__[i])
            self.assertTrue(np.all(np.equal(correct[i], output)))

class genSchdExceptions(GenSchdTestSetUp):
    """
    Raise exceptions under conditions defined by the requirements.
    """    
    def test_ExceptionsGenSchd(self):
        self.assertRaises(ValueError, hF.genSchd, 0)
        self.assertRaises(ValueError, hF.genSchd, -1)
        self.assertRaises(ValueError, hF.genSchd, 33)

if __name__ == '__main__':
    unittest.main()
