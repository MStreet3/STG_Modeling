# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 11:55:06 2014

@author: mstreet
"""

import numpy as np


cases = np.array(xrange(1,4))
H_v = np.array([1200, 2400, 3600])
H_is = np.array([15.525, 31.05, 46.575])
H_ms = np.array([9.1, 18.2, 27.3])
H_em = np.array([1.12345679, 2.246913581, 3.370370375])
H_tr_i = np.array([1.0, 4.0, 9.0])
H_g = np.array([1.6, 5.2, 10.8])
H_1 = np.array([15.32671068, 30.65342136, 45.98013204])
H_2 = np.array([16.32671068, 34.65342136, 54.98013204])
H_3 = np.array([5.843188647, 11.93285605, 18.24204176])
theta_m = np.array([1,2,3])
theta_op = np.array([2.4, 2, 1.6])


b = H_ms + H_tr_i + H_1
q = cases + cases
c = cases + q/H_v
a = H_ms*theta_m + cases + H_tr_i*cases + H_1*c
theta_s = a/b

num = H_is*theta_s + H_v*cases + cases + cases
den = H_is + H_v
theta_i = num/den

