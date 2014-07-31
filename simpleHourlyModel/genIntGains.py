# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:19:07 2014

@author: mstreet
"""
import numpy as np
import helpFncs
from classes import errorClassesSHM as EC
import pdb
# Based on the peak gains and schedule fraction for the year, this script
# generates an Nx2 array of phi_int to be passed to the building demand 
# model.


def genIntGains(A_floor, occDen, actLev, oc_schd_wd, oc_schd_we,
                appDen, outAir, app_schd_wd, app_schd_we,
                lightDen, light_schd_wd, light_schd_we,
                start = (1,1,1), stop = (12,31,24), startDay = 1,               
                procDen = 0, proc_schd_wd = None, proc_schd_we = None,
                adjDen = 0, adj_schd_wd = None, adj_schd_we = None,
                qH2O = 0, H2Olen = 0, H2O_schd_wd = None, H2O_schd_we = None,
                qHVAC = 0, HVAClen = 0,
                HVAC_schd_wd = None, HVAC_schd_we = None):
        """
        Inputs:
        
        gross conditioned floor area [m2]
        occupancy peak [m2/person]
        metabolic rate [w/person]
        appliance peak [W/person]
        lighting peak [w/person]
        outdoor air infiltration [L/s/person]
        domestic hot water not used in thermal demand calculation
        
        Output:
        print type(SchdList)
        phi_int - internal gain at each hour [w]
        vflo - infiltration flow rate at each hour [m3/s]
        
        calcQ_int(phi_oc, phi_app, phi_light, phi_wa, phi_hvac, phi_proc,
                      phi_adj, adjFac = 0.5)
        
        calcPhi_oc(occDen, area, actLev, schFra) - phi_oc
        
        calcPhi_gen(peaDen, area, schFra) - phi_proc, phi_app, phi_light, phi_adj
        
        calcPhi_genDis(qAvg, lenDis, schFra) - phi_hvac, phi_wa
        
        """

        __ = [[oc_schd_wd, app_schd_wd, light_schd_wd, 
              proc_schd_wd, adj_schd_wd, H2O_schd_wd,
              HVAC_schd_wd],
              [oc_schd_we, app_schd_we, light_schd_we, 
               proc_schd_we, adj_schd_we, H2O_schd_we,
               HVAC_schd_we]]
        
        SchdList = []
        for i in range(len(__)):
            SchdList.append([schd for schd in __[i] if schd != None])
        
        
        # need the occ, app, and light schedule for both weekday and weekends.
        # need the total conditioned floor area
        # need the occDen, actLev
        # need the peak density of appliances and lighting
        # need the outdoor air rate
        # need the adjacent peak rate, hvac length, pipe lengths and avg q for
        #       hvac and plumbing.
        
        # which hours are we calculating?
        hIndex = np.array(helpFncs.timeDiff(start, stop))

        # how many hours are we calculating?
        nHours = len(hIndex)
        dIndex = np.array(helpFncs.genDayIndex(startDay, nHours))
        
        # For that many days (given the start Day) generate the schedule for
        # occ, lights, and appliances.  Should be a matrix that is n hours long 
        # by 7 columns.  Accounts for weekends and weekdays.
        
        hourData = np.zeros((nHours, 2 + sum(map(len, SchdList))))
        
        hourData[:, 0:2] = [hIndex.reshape((nHours,1)), 
                            dIndex.reshape((nHours,1))]
        
        
        
            
            
            
        
        # calculate the phi_oc with the appropriate schedule.
        
        # calculate the general gains with the appropriate schedule.
        #   if peak density is zero, dont't require a schedule. 
        
        # calculate the distribution gains with appropriate schedules.
        #   if either length or average q is zero do not require a schedule.
        
        # pass each of the vectors to the summation function.
        
        # return a vector that is n hours by 2 which is the q int at each desired
        # hour and the H_ven.
        
        return 0

genIntGains(1,1,1,np.ones(24),np.ones(24),
                1, 1, np.ones(24), np.ones(24),
                1, np.ones(24), np.ones(24),
                start = (1,1,1), stop = (12,31,24), startDay = 1)

print 'test'


#print getIntGains