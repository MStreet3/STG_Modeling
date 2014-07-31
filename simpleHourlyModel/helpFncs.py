# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 12:11:34 2014

@author: mstreet
"""
import numpy as np
import pdb

def dateConvert(month, day):
    """
    Convert the month and day to day of year.
    """    
    day_in_month = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    months = np.arange(1,13)
    days = np.arange(1, 366)
    
    if month not in months:
        raise ValueError('Month must be integer between 1 and 12.')
    
    if day not in np.arange(1,day_in_month[month-1]+1):
        raise ValueError('Day ' + str(day) + ' not in range for Month '
                   + str(month) + '.  Must be an integer between 1 and ' 
                   + str(day_in_month[month-1]))
    
    
    if month == 1:
        DoY = day
    else:
        DoY = sum(day_in_month[:month-1])+day
    
    if DoY not in days:
        raise ValueError('The date ' + str(DoY) + ' is not in the range of'
         + ' 1 to 365.')
    
    return DoY
    
def genSchd(startDay):
    """
    Given start day of the year return the week.  Will need to be tiled to 
    generate the pattern for arbitrary number of days. (multiple of 7)
    
    """
    week = np.arange(1,8)    
    if startDay not in week:
        raise ValueError('Invalid start day for the week.')

    __ = np.append(week[startDay-1:], week[:startDay-1])

    return __
def genDayIndex(startDay, nHours):
    """
    Return list of days that is as long as nHours.  Indicates for each hour
    the day of the week it belongs to.
    
    """
    
    dIndex = []
    hours = 0
    count = 0
    while hours < nHours:
        base = genSchd(startDay)
        if hours > 0 and hours%24 == 0:
            if count > len(base)-1:
                count = 0
            else:
                count += 1
        
        dIndex.append(base[count])
        hours += 1
    
    return dIndex

def hourOfYear(dateTuple):
    """
    Return the hour of the year given a tuple of (month, day, hour).
    """
    yearDay = dateConvert(dateTuple[0],dateTuple[1])
    if yearDay == 1:
        yearHour = dateTuple[2]
    else:
        yearHour = (yearDay - 1)*24 + dateTuple[2]
    
    return yearHour

def stackSchedules(nHours, wdSchd, weSchd, startDay):
    """
    Stack the schedules from each list based on whether weekday or weekend.
    """
    holder = []
    base = genSchd(startDay)
    
    schInd = 0
    dayInd = 0
    count = 0

    while count < nHours:
        
        if schInd > 23:
            schInd = 0
            if dayInd > 6:
                dayInd = 0
            dayInd += 1      
              
        if base[dayInd] in range(2,7):
            holder.append(wdSchd[schInd])
        else:
            holder.append(weSchd[schInd])
        
        schInd += 1
        count += 1
    
    return np.array(holder)
        
        
    
def timeDiff(start, stop):
    """
    Convert two tuples of (month, day, hour) into the number of hours between
    each hour.  Includes the start hour and the last hour.  Returns an index
    of the hours.
    
    """
    
    dates = [start, stop]
    hours = []
    
    for date in dates:
        hours.append(hourOfYear(date))
    
    a = range(hours[0])
    b = range(hours[-1])
    
    hIndex = b[len(a)-1:]
    
    return hIndex
