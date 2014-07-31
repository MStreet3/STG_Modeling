# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 17:23:03 2014

@author: mstreet
"""
from collections import namedtuple
import numpy as np

def dayAngle(day):
    """
    Calculation of day angle per equation 1.2.2 of An Introduction to Solar
    Radiation by Iqbal.
    
    Input:
    
    day - " Day number of the year, ranging from 1 on 1 January to 365 on 31
            December.  February is always assumed to have 28 days."
            
    Output:
    
    B - day angle in radians.
    """
    B = 2.*np.pi*(day - 1.)/365.
    return B

def declinAng(B):
    """
    Position of the sun relative to the Earth's axis.  Detailed description
    from §1.3 and equation 1.3.1 of An Introduction to Solar Radiation
    by Iqbal. 
    
    Input:
        
    B - the day angle in radians
    
    Output:
    
    decAng - declination angle in degrees.
    
    """

    decAng = (0.006918 - 0.399912*np.cos(B) + 0.070257*np.sin(B)
                - 0.006758*np.cos(2.*B) + 0.000907*np.sin(2.*B)
                - 0.002697*np.cos(3.*B) + 0.00148*np.sin(3.*B))*(180./np.pi)
    
    return decAng

def eqnOfTime(B):
    """ 
    Discrepancy between clock time and sun location in minutes.  See §1.4 and
    equation 1.4.1 of An Introduction to Solar Radiation by Iqbal.  
    
    Input:
        
    B - the day angle in radians.
    
    Output:
        
    Eot - equation of time in minutes.
    
    """
    EoT = (0.000075 + 0.001868*np.cos(B) - 0.032077*np.sin(B)
            - 0.014615*np.cos(2.*B) - 0.04089*np.sin(2.*B))*(229.18)
    return EoT

def timeCorrectionFactor(lon, EoT, UTCoff, DST = 0):
    """ 
    Function returns the correction factor for a longitude and EoT.  Correction
    factor is seen in equation 1.4.2 of An Introduction to Solar Radiation by
    Iqbal.  Measure of minutes to be added algebraically to local standard
    time to determine the local apparent solar time at a particular hour.  By
    default the hour is assumed to not be in observance of Daylight Savings 
    Time (DST).
        
    
    Input:
        
    lon - site longitude in decimal degrees.
    EoT - equation of time in minutes. [min]
    UTCoff - site timezone defined as hour offset relative to UTC. [h]
    DST - integer flag to indicate if the current hour is in observance of DST.
    
    Output:
    
    TC - time offset from true solar time. [min]
    

    """
    if DST:
        TC = EoT - 4.*lon + 60.*UTCoff - 60 # Subtract an additional 60 mins.
    else:
        TC = EoT - 4.*lon + 60.*UTCoff     
    return TC

def localSolarTime(locTime, timeCorr):
    """
    Local solar time given the local time and time correction factor in 
    decimal hours.
    
    Input:
        
    locTime - local time in decimal hours
    timeCorr - time correction for longitude and time zone in minutes
    
    """
    
    LST = locTime + timeCorr/60.
    return LST
    
def hourAngle(locSolTime):
    """
    Calculate the sun's hour angle.
    
    locSolTime - Local solar time in decimal hours.
    """
    HRA = 15*(locSolTime - 12)
    return HRA

def surfaceDirectIrradiation(decAngle, lat, tilt, azi, HRA, DNI):
    """
    Calculate the hourly, beam irradiation on an arbitrarily oriented surface 
    on Earth.  Follows the equations from An Introduction to Solar Radiation by
    Iqbal.  See Eqns. 11.2.9, 1.5.1, and 1.6.5a
    
    Input:
    
    decAngle (delta) - Earth's declination angle.
    lat      (phi)   - site latitude in decimal degrees, north positive.
    tilt     (beta)  - object tilt in degrees
    azi      (gamma) - object azimuth in degrees
    HRA      (omega) - hour angle of the sun in degrees taken at the hour's 
                       midpoint.
    DNI              - average hourly normal irradiance on the surface [Wh/m2]
    
    Output:
    
    B                - Average power over the hour on an arbitrarily oriented 
                       surface. [Wh/m2]    
    """
    # Unit Conversions
    
    decAngle = np.pi*decAngle/180.
    lat      = np.pi*lat/180.
    tilt     = np.pi*tilt/180.
    azi      = np.pi*azi/180.
    HRA      = np.pi*HRA/180.    
    
    # Calculations
    
    cosTheta_z = np.sin(decAngle)*np.sin(lat) + np.cos(decAngle)*np.cos(lat)\
    *np.cos(HRA)
    
    cosTheta =  ((np.sin(lat)*np.cos(tilt) - np.cos(lat)*np.sin(tilt)*np.cos(azi))*np.sin(decAngle)
         + (np.cos(lat)*np.cos(tilt) +  np.sin(lat)*np.sin(tilt)*np.cos(azi))*np.cos(decAngle)*np.cos(HRA)
         +  np.cos(decAngle)*np.sin(tilt)*np.sin(azi)*np.sin(HRA))   
    
    B = DNI*cosTheta/cosTheta_z
    return B

def surfaceDiffuseIrradiation(tilt, DHI):
    """
    Average diffuse irradiation on a tilted surface. [Wh/m2]
    
    tilt - surface tilt angle. [deg]
    DHI - Average diffuse irradiation on a horizontal surface. [Wh/m2]
    
    """
    
    D = DHI*((180.-tilt)/180.)
    
    return D

def surfaceGroundIrradiation(Itotal, rho, tilt):
    """
    Hourly ground reflected energy on a surface assuming an isotropic sky
    distribution and identical surface reflectance to both beam and sky diffuse
    radiation.  From An Introduction to Solar Radiation by Iqbal.  See
    eqn. 11.3.4.
    
    Input:
    
    Itotal - sum of diffuse and beam radiation on surface. [Wh/m2]
    rho    - surface reflectance.
    tilt   - Surface angle with horizontal plane/surface inclination. [deg]
    
    Output:
    """

    Ir = 0.5*Itotal*rho*(1. - np.cos(tilt*np.pi/180.))

    return Ir    
    
def surfaceIrradiation(lat, lon, tilt, azi, rho, DNI, DHI, day, locTime, UTC,
                       DST):
    """

    Calculate the diffuse, direct, and ground reflected energy incident on a 
    surface. [Wh/m2]
    
    Input:
    
    lat     - latitude of site in decimal degrees
    lon     - longitude of site in decimal degrees
    tilt    - surface tilt in degrees (0 - horizontal, 90 - vertical)
    azi     - surface azimuth in degrees (0 - S, 90 - E, 180 - N, -90 - W)
    rho     - surface reflectance
    DNI     - hourly average direct solar irradiation normal to a horizontal 
              surface [W/m2]
    DHI     - hourly average diffuse solar irradiation on a horizontal surface
              [W/m2]
    day     - julian day corresponding to data
    locTime - Time in decimal hours corresponding to irradiation data.  For 
              hourly average data, the midpoint local time should be used.
    UTC     - UTC offset of the timezone. 
    DST     - Integer flag indicating if current hour is under observance of 
              Daylight Savings Time (DST). [1 or 0]
    
    Output:    
    Returns a namedtuple with fields
        1. Ibeam - Wh/m2 on arbitrarily tilted surface of DNI
        2. Idiff - Wh/m2 on arbitrarily tilted surface of DHI
        3. Irec  - Wh/m2 of ground reflected energy received on same surface.
    
    """
    dayAng = dayAngle(day)
    decAng = declinAng(dayAng)
    EoT = eqnOfTime(dayAng)    
    TC = timeCorrectionFactor(lon, EoT, UTC, DST)
    LST = localSolarTime(locTime, TC)
    HRA = hourAngle(LST)
    dniSur = surfaceDirectIrradiation(decAng, lat, tilt, azi, HRA, DNI)
    dhiSur = surfaceDiffuseIrradiation(tilt, DHI)
    Itot = dniSur + dhiSur
    Irec = surfaceGroundIrradiation(Itot, rho, tilt)
    
    TiltedSurface = namedtuple('TiltedSurface', 'Ibeam, Idiff, Irec')
    
    surIrrad = TiltedSurface(dniSur, dhiSur, Irec)
    
    return surIrrad
    
    
    
    