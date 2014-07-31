# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:25:56 2014

@author: mstreet
"""
from pysolsurface import solarEqns as se
import numpy as np
import annexCeqns as ISO

# Based building, site, and start and stop information this script will
# generate the hourly DHI and DNI on every eligible surface of the building.
# Then this data will be used to generate Q sol at each hour for each surface.


def genSolGains(building, site, start = (1,1,1), stop = (12,31,24)):
    """
    Calculates the total solar gains for a building a specified site over a 
    defined calculation period.  From the standard, the sources to consider
    are:    
    
    "The collecting areas to be taken into consideration are the glazing 
    (including any integrated or add-on solar shading provision), the external
    opaque elements, the internal walls and floors of sunspaces, and walls
    behind a transparent covering or transparent insulation."
    
    Inputs:
    
    building - a building object
    site - a site object
    start - tuple of month, day, and hour indicating calculation start time
    stop - tuple of month, day, and hour indicating calculation end time
    
    Output:
    qSol - total solar gains per ISO 13790 at each hour to pass to
            calcBuildingDemand
    
    """
    pass