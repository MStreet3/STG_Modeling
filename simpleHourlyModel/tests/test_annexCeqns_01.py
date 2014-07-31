# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:11:22 2014

@author: mstreet
"""

import unittest
import numpy as np
import annexCeqns as ISO
# import pdb

class ISOtestSetUp(unittest.TestCase):
    def setUp(self):
        self.cases = np.array(xrange(1,4))
        # transmission coefficients
        self.H_v = np.array([1200, 2400, 3600])
        self.H_is = np.array([15.525, 31.05, 46.575])
        self.H_ms = np.array([9.1, 18.2, 27.3])
        self.H_em = np.array([1.12345679, 2.246913581, 3.370370375])
        self.H_tr_i = np.array([1.0, 4.0, 9.0])
        self.H_g = np.array([1.6, 5.2, 10.8])
        self.H_1 = np.array([15.32671068, 30.65342136, 45.98013204])
        self.H_2 = np.array([16.32671068, 34.65342136, 54.98013204])
        self.H_3 = np.array([5.843188647, 11.93285605, 18.24204176])
        
        # temperatures
        self.theta_m = np.array([1,2,3])
        self.theta_s = np.array([1.03932872, 2.0378405, 3.03646081])
        self.theta_i = np.array([ 1.0021477 ,  2.00212869,  3.00211107])
        self.theta_op = np.array([2.4, 2, 1.6])
        
        # power
        self.Q_ia = np.array([0.5, 1, 1.5])
        self.Q_m = np.array([1.5, 3, 4.5])
        self.Q_st = np.array([-0.164835165, -0.32967033, -0.494505495])
        self.Q_mtot = np.array([7.0, 20.0, 39.0 ])
        self.Qint = np.array([6.5, 13., 19.5])
        
        # misc
        self.knownC_m = np.array([80000.0,110000.0,165000.0,260000.0,370000.0])
        self.knownA_m = np.array([2.5,2.5,2.5,3.0,3.5])
        self.knownB_prime = np.array([2, 2, 2])
        self.knownDt = np.array([7,14,21])
        self.numClass = np.array(range(1,6))
        
    def tearDown(self):
        self.cases = None

class ConductanceEqnTestCaseKnownVal(ISOtestSetUp):
    """ Eqns. should give known result with known input. """
    def test_H_v(self):
        
        self.assertTrue(np.allclose(ISO.calcH_vent(V_flo = self.cases),
                                    self.H_v))
    
    def test_H_is(self):
       
        self.assertTrue(np.allclose(ISO.calcH_is(A_fl = self.cases),
                                    self.H_is))
    
    def test_H_ms(self):
        
        self.assertTrue(np.allclose(ISO.calcH_ms(A_m = self.cases), 
                                    self.H_ms))
    
    def test_H_em(self):
        
        self.assertTrue(np.allclose(ISO.calcH_em(H_op = self.cases, 
                                    H_ms = np.array([9.1, 18.2, 27.3])),
                                    self.H_em))
                        
    def test_H_tr_i(self):
       
        self.assertTrue(np.allclose(ISO.calcH_tr_i(A_i = self.cases,
                                                   U_i = self.cases), 
                                    self.H_tr_i))

    def test_H_g(self):
        
        self.assertTrue(np.allclose(ISO.calcH_g(A_e = self.cases,
                                                U_g = self.cases, 
                                                P_e = self.cases), 
                                    self.H_g))
    
    def test_H_1(self):
        
        self.assertTrue(np.allclose(ISO.calcH_1(H_v = self.H_v,
                                                H_is = self.H_is),
                                    self.H_1))
    
    def test_H_2(self):
        
        self.assertTrue(np.allclose(ISO.calcH_2(H_1 = self.H_1,
                                                H_win = self.H_tr_i),
                                    self.H_2))
    
    def test_H_3(self):
        
        self.assertTrue(np.allclose(ISO.calcH_3(H_2 = self.H_2,
                                                H_ms = self.H_ms), 
                                    self.H_3))                                              
                                
class TemperatureEqnTestCaseKnownVal(ISOtestSetUp):
    """ Eqns. should give known result with known input. """
    def test_Theta_m(self):
        
        self.assertTrue(np.allclose(ISO.calcTheta_m(theta_mt = self.cases,
                                                    theta_mt_1 = self.cases),
                                    self.theta_m))
    def test_Theta_s(self):
        
        self.assertTrue(np.allclose(ISO.calcTheta_s(Q_st = self.cases,
                                                    Q_ia = self.cases,
                                                    Q_d = self.cases,
                                                    H_ms = self.H_ms,
                                                    H_win = self.H_tr_i,
                                                    H_v = self.H_v,
                                                    H_1 = self.H_1,
                                                    theta_e = self.cases,
                                                    theta_airin = self.cases,
                                                    theta_m = self.theta_m),
                                    self.theta_s))         

    
    def test_Theta_i(self):
        
        self.assertTrue(np.allclose(ISO.calcTheta_i(Q_ia = self.cases,
                                                    Q_d = self.cases,
                                                    H_is = self.H_is,
                                                    H_v = self.H_v,
                                                    theta_s = self.theta_s,
                                                    theta_airin = self.cases),
                                    self.theta_i))
                                    
    
    def test_Theta_op(self):
        reverse = self.cases[::-1]
        self.assertTrue(np.allclose(ISO.calcTheta_op(theta_i = self.cases,
                                                     theta_s = reverse),
                                    self.theta_op))   
    
    
class PowerEqnTestCaseKnownVal(ISOtestSetUp):
    """ Eqns. should give known result with known input. """
    def test_calcQ_ia(self):
        """ Check order of operations of equation C.1 of ISO 13790 """
        self.assertTrue(np.allclose(ISO.calcQ_ia(Q_int = self.cases),
                                    self.Q_ia))
        
    def test_calcQ_m(self):
        """ Check order of operations of equation C.2 of ISO 13790 """
        self.assertTrue(np.allclose(ISO.calcQ_m(Q_int = self.cases,
                                                Q_sol = self.cases,
                                                A_m = self.cases,
                                                A_t = self.cases),
                                    self.Q_m))
    def test_calcQ_st(self):
        """ Check order of operations of equation per C.3 of ISO 13790 """
        self.assertTrue(np.allclose(ISO.calcQ_st(Q_int = self.cases,
                                                 Q_sol = self.cases,
                                                 A_m = self.cases,
                                                 A_t = self.cases,
                                                 H_es = self.cases),
                                    self.Q_st))       
        
        
    def test_calcQ_mtot(self):
        
        """ Check order of operations of equation C.5 of ISO 13790 """        
        self.assertTrue(np.allclose(ISO.calcQ_mtot(Q_m = self.cases,
                                                   Q_st = self.cases,
                                                   Q_ia = self.cases,
                                                   Q_d = self.cases,
                                                   H_em = self.cases,
                                                   H_win = self.cases,
                                                   H_v = self.cases,
                                                   H_1 = self.cases,
                                                   H_2 = self.cases,
                                                   H_3 = self.cases,
                                                   theta_e = self.cases,
                                                   theta_airin = self.cases),
                                    self.Q_mtot))
    def test_calcQ_int(self):
        """
        Check order of operations on equation 35 of ISO 13790-2008 10.2.2
        """
        intGain = ISO.calcQ_int(phi_oc = self.cases,
                            phi_app = self.cases,
                            phi_light = self.cases,
                            phi_wa = self.cases,
                            phi_hvac = self.cases,
                            phi_proc = self.cases,                           
                            phi_adj = self.cases)
        self.assertTrue(np.allclose(intGain, self.Qint))
        

class MiscEqnTestCase(ISOtestSetUp):
    
    def test_calcA_mKnownVal(self):
        """ A_m must produce the known output for a unit area. """
        index = 0
        for num in self.numClass:
            self.assertTrue(np.allclose(ISO.calcA_m(A_f = 1, 
                                                classNum = num),
                                    self.knownA_m[index]))
            index += 1
            
    def test_calcC_mKnownVal(self):
        """ C_m must produce the known output for a unit area. """
        index = 0
        for num in self.numClass:
            self.assertTrue(np.allclose(ISO.calcC_m(A_f = 1, 
                                                classNum = num),
                                    self.knownC_m[index]))
            index += 1
    def test_B_primeKnownVal(self):
        """ Must produce known value from test """
        index = 0
        for num in self.cases:
            self.assertTrue(np.allclose(
                            ISO.calcB_prime(A_e = self.cases[index],
                            P_e = self.cases[index]), self.knownB_prime[index])
                            )
            index += 1
    def test_CalcDtKnownVal(self):
        """ Must produce known value from test """
        index = 0
        for num in self.cases:
            self.assertTrue(np.allclose(
                            ISO.calcDt(w = self.cases[index],
                                       R_si = self.cases[index],
                                       R_f = self.cases[index],
                                       R_se = self.cases[index]),
                             self.knownDt[index]))
            index += 1

    def test_calcA_mBadInput(self):
        """ A_m must fail if class selector is out of range. """
        self.assertRaises(ValueError, ISO.calcA_m, self.cases, 10)
        
        """ A_m must fail for negative values of the area. """
        self.assertRaises(ValueError, ISO.calcA_m, -self.cases, 2)
        
    def test_calcC_mBadInput(self):
        """ C_m must fail if class selector is out of range. """
        self.assertRaises(ValueError, ISO.calcC_m, self.cases, 10)
        
        """ C_m must fail for negative values of the area. """
        self.assertRaises(ValueError, ISO.calcC_m, -self.cases, 2)

    def test_calcU_gBadInput(self):
        """ U_g must fail for characteristic lengths less than zero. """
        self.assertRaises(ValueError, ISO.calcU_g, -self.cases, self.cases)
        self.assertRaises(ValueError, ISO.calcU_g,  self.cases, -self.cases)
        self.assertRaises(ValueError, ISO.calcU_g, 0, self.cases)
        
    def test_calcB_primeBadInput(self):
        """ B_prime must fail if either input is less than zero. """
        self.assertRaises(ValueError, ISO.calcB_prime, -self.cases, self.cases)
        self.assertRaises(ValueError, ISO.calcB_prime, self.cases, -self.cases)
        self.assertRaises(ValueError, ISO.calcB_prime, 0, self.cases)
    
    def test_calcDt_BadInput(self):
        """ Dt must fail if all arguments are not greater than zero. """
        pass
#        self.assertRaises(ValueError, ISO.calcDt, -self.cases, self.cases)        
#        self.assertRaises(ValueError, ISO.calcDt, self.cases, -self.cases)        
#        self.assertRaises(ValueError, ISO.calcDt, self.cases, 0)
     

if __name__ == "__main__":
    unittest.main()

