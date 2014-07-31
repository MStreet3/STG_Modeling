# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 16:26:12 2014

@author: mstreet
"""
import pdb


class ConstructionMaterial():
    """
    Class for defining a solid material.
    
    """
    def __init__(self, cp, k, dens, absSol, emiLon):
        self.cp = cp
        self.k = k
        self.dens = dens
        self.absSol = absSol
        self.emiLon = emiLon
        
class ConstructionLayer():
    """
    Class for defining opaque surfaces.
    
    """
    
    def __init__(self, tilt, azimuth, area, dT, material):
        assert isinstance(material, ConstructionMaterial)        
        self.tilt = tilt
        self.azi = azimuth
        self.area = area
        self.dT = dT
        self.matProps = material
        self.Rval = self.matProps.k/self.dT
        self.Uval = 1./self.Rval

class BuiltUpSurface():
    """
    Class for defining a system of layers.  Each layer must be of the class
    ConstructionLayer and must have the same tilt, azimuth, and area.
    
    Total resistance is calculated by adding summing the series.
    
    Build the surface from outside to inside.
    
    """
    surf = []
    def __init__(self, layers = []):
        tilt = []
        azi = []
        area = []
        for layer in layers:
            assert isinstance(layer, ConstructionLayer)
            self.surf.append(layer)
            tilt.append(layer.tilt)
            azi.append(layer.azi)
            area.append(layer.area)

        sameTilt = len(set(tilt)) <= 1
        sameAzi  = len(set(azi)) <= 1
        sameArea = len(set(area)) <= 1
        
        assert sameTilt and sameAzi and sameArea
        
        self.Rtot = sum([layer.Rval for layer in self.surf[:]])
        self.Utot = 1./self.Rtot
        self.tilt = self.surf[0].tilt
        self.area = self.surf[0].area
        self.azi = self.surf[0].azi
        self.extSur = self.surf[0]
        self.intSur = self.surf[-1]

class ZoneEnvelope():
    """
    Class for defining the envelope of a simple zone.  Separates envelope 
    constructions into BuiltUpSurfaces that act as solar sources and those 
    that do not.
    """
    zoneSol = []
    zoneInt = []
    
    def __init__(self, volume, conFlrArea, solar = [], internal = []):
        self.vol = volume
        self.Aflr = conFlrArea
        for surface in solar:
            assert isinstance(surface, BuiltUpSurface)
            self.zoneSol.append(surface)
        
        for surface in internal:
            assert isinstance(surface, BuiltUpSurface)
            self.zoneInt.append(surface)
        
class ZoneSchedule():
    """
    Class to store generic 24 hour fractional schedule data.
    """
    def __init__(self, fraction):
        # need to make sure it is only 24 long
        # need to make sure this is only values between 0 and 1.
        self.schdFrac = fraction 

class BuildingSite():
    """
    Class to store some site variables for the building.
    
    """
    def __init__(self, lon, lat, UTC, DST = 0,
                 DSTstart = None, DSTstop = None, weaFileType = 'EPW',
                 weaFilePath = None):
                     self.lon = lon
                     self.lat = lat
                     self.UTC = UTC
                     self.DST = 0
                     self.DSTstart = DSTstart
                     self.DSTstop = DSTstop
                     self.weaFileType = weaFileType
                     self.weafilePath = weaFilePath

                     

#conc = ConstructionMaterial(1,1,1,1,1)
#
#extSur = ConstructionLayer(90.,0.,1,1,conc)
#intSur = ConstructionLayer(90,0.,1,1,conc)
#
#southWall = BuiltUpSurface([extSur,intSur])
#pdb.set_trace()       
        
        