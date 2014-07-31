# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 17:02:42 2014

@author: mstreet
"""
import pdb
def foo(a, b = a):
    c = a+b
    pdb.set_trace()
    return c