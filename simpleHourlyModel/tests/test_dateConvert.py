# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 11:44:02 2014

@author: mstreet
"""
# Requirements
# dateConvert should be an ideal function that returns a value between 1 and 
#             365. (1 <= year <= 365)
# dateConvert should accept an integer representation of the month and an 
#             integer representation of the day. (1 <= day <= 31)
# dateConvert should raise ValueError if either of these condtions is not met.
# dateConvert should produce known output for known input.

import unittest
import numpy as np
from simpleHourlyModel import helpFncs as hF

 
class DateConvertTestSetUp(unittest.TestCase):
    """
    Define some common set up procedures.
    
    """
    
    def setUp(self):
        self.months = np.arange(1,13)
        self.days = np.ones(len(self.months), dtype = np.int)
        

class DateConvertKnownValues(DateConvertTestSetUp):
    """
    Function gives known values for known input.
    
    """
    def test_KnownInputDateConvert(self):    
        __ = [1,32,60,91,121,152,182,213,244,274,305,335]
        correct = np.array(__)

        for i in range(len(__)):
            output = hF.dateConvert(self.months[i], self.days[i])
            self.assertTrue(np.all(np.equal(correct[i], output)))

class DateConvertExceptions(DateConvertTestSetUp):
    """
    Raise exceptions under conditions defined by the requirements.
    """
    
    def test_ExceptionsDateConvert(self):
        self.assertRaises(ValueError, hF.dateConvert, 15, 1)
        self.assertRaises(ValueError, hF.dateConvert, 1, 33)
        self.assertRaises(ValueError, hF.dateConvert, 2, 33)

if __name__ == '__main__':
    unittest.main()
