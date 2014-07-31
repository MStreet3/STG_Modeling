# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:10:57 2014

@author: mstreet
"""
import simpleHourlyModel as shm

def calcClinicDemand(floorArea, start, stop):
    # function stub for the clinic to hash out how this should work

        # First instantiate the default building based on the floor area.
        """ needs a call to a class constructor function. """
        
        # Bring in the appropriate weather data
            # needs a function to read the weather data from EPW file.
            # In general, this could be a method of the BuildingSite class,
            # which means here I just call the method.            
        
        # Generate the internal gains for the time period
        """ need a call to the funciton getIntGains. """
            # shm.genIntGains comes back with Nx2 array
            
        # Generate the solar gains for the time period
        """ need a call to the function getSolGains. """
            # shm.getSolGains comes back with Nx1
        
        # for hour in range(len(solgainsresults)):
        # run the calcBuildingDemand function for the time period
        # with the local variables call the function calcBuildingDemand.
            # calcBuildingDemand still requires another wrapper and then must
            # be called within a loop.
        
        # return the building demand at each hour
        """ Let user define what they want to do with the resulting vector. """
        
        pass