# -*- coding: utf-8 -*-
"""
Created on Wed Jul 09 14:04:45 2014

@author: mstreet
"""

class isoSHMError(Exception):
    pass

class TempOutOfBoundError(isoSHMError):
    pass

class ZoneResponseError(isoSHMError):
    pass

class ScheduleError(isoSHMError):
    pass