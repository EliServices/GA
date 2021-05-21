def getvar():
    setti = ["0","49.999999","49.000000","8.999999","8.000000","lxml","95"]
    #Settings:
    #0: showoffline    : 1 = true, 0 = false
    #   show offline aircrafts
    #
    #1 - 4: coordinates: Coordinates define the square for the system to work in.
    #                    7 decimal places needed.
    #                    Coordinates in °S must be converted in °N. For example: 7°S = -7°N.
    #                    Same goes for west and east, e.g.: 5°W = -5°E.
    #1: maxlat         : higher latitude in °N
    #2: minlat         : lower latitude in °N
    #3: maxlong        : higher longitude in °E
    #4: minlong        : lower longitude in °E
    #Note: Coordinates (49.°N, 49.0°N, 8.9°E, 8.0°E) are for EDFM airport.
    #
    #5: rtype          : type of the request that is supposed to be sent, options: "lxml" "livexml" "data"
    #   request type
    #Note: "lxml" is default.
    #
    #6: MSL altitude of the airport in meter, EDFM is at around 95m.
    return setti
