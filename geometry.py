#Library containing tools for geometrical operations and coordinate systems v.1
#First, we define some things that will be needed several times in the code.
def geometry_version():
    return "v1, 03/2021"

from . import settings
from . import floatmath

def floating(se): #This converts the last 5 positions for a list with 6 positions into floats that have a maximum
    for l in range(1,5):                                                             # of 7 digits behind the dot.
        se[l] = float(se[l])
        se[l] = round(se[l],7)
    return se

def geos(): #Additional numbers for geographical work
    set_geo = settings.getvar() #General information
    set_geo = floating(set_geo) #Fix for dataissues

    step = float("0.0000001")
    diflat = floatmath.subtract(set_geo[1], set_geo[2])  #Difference between °N coordinates given from settings
    diflong = floatmath.subtract(set_geo[3], set_geo[4]) #Difference between °E coordinates given from settings
    mer = 40007.863                   #Length of a meridian                 #in km: equator, 0-Meridian, +1°N in km
    retvalue = [step, int(round(diflat,6)*1000000), int(round(diflong,6)*1000000), 40075.017, mer, round(mer/360,3)]
    return retvalue

def deg_sysco(la, lon): #Converts degree to system coordinates(latitude, longitude)
    #fl = ["0.0", float(la), float(lon)]
    #set_geo = settings.getvar() #General information
    #set_geo = floating(set_geo) #Fix for dataissues

    #la = floatmath.subtract(fl[1], set_geo[2])*1000000  #Actual converting into our own coordinates
    #lon = floatmath.subtract(fl[2], set_geo[4])*1000000
    la = str(la)
    lon = str(lon)
    x1 = la.find(".")
    x2 = lon.find(".")
    la = la[x1+1:]
    lon = lon[x2+1:]

    re = [int(la), int(lon)]
    return re

def sysco_deg(regla, reglon): #Converts ystem coordinates to degree(x, y)
    fl = ["0.0", float(regla), float(reglon)]
    set_geo = settings.getvar() #General information
    set_geo = floating(set_geo) #Fix for dataissues

    regla = floatmath.add((fl[1]/1000000), set_geo[2]) #Actual converting into usual coordinates
    reglon = floatmath.add((fl[2]/1000000), set_geo[4])
    re = [regla, reglon]
    return re

def radius_deg(latitu): #Calculates the circumferenz of any latitude
    import math
    geom = geos()

    radian = math.radians(latitu)
    co = math.cos(radian)
    co2 = co * co
    si = math.sin(radian)
    si2 = si * si
    rad1 = geom[3]*geom[4]*co
    rad2 = math.sqrt((geom[3] * geom[3] * si2) + (geom[4] * geom[4] * co2))
    rad3 = rad1 / rad2
    return rad3

def radius_sysco(sysco): #Calculates the circumferenz of any system coordinate
    deg = sysco_deg(sysco, 8.0)
    radix = radius_deg(deg[0])
    return radix
