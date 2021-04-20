def bubblesort(lis):
    x = len(lis)
    lis.append("20001")
    inp = []
    num = []
    for i in range(0,x+1):
        inp.append(lis[i][4])

    finish = 0
    while finish == 0:
        finish = 1
        for k in range(0,x):
            if int(inp[k]) > int(inp[k+1]):
                y = lis[k]
                lis[k] = lis[k+1]
                lis[k+1] = y
                yy = inp[k]
                inp[k] = inp[k+1]
                inp[k+1] = yy
                finish = 0
    lis.remove("20001")
    return lis

def extract_position(rawda):
    in_square = []
    for i in range(0,len(rawda)):
        lat = float(rawda[i][0])
        lon = float(rawda[i][1])
        if lat > 49.449:
            if lat < 49.501:
                if lon > 8.459:
                    if lon < 8.581:
                        in_square.append(rawda[i])
    return in_square

def bytype(type,aircrafttype,planes,altitude,rawda):
    altitude_out = []
    planes_out = []
    rawdata_out = []
    for i in range(0,len(aircrafttype)):
        if aircrafttype[i] == type:
            altitude_out.append(altitude[i])
            planes_out.append(planes[i])
            rawdata_out.append(rawda[i])
    bytype.altitude = altitude_out
    bytype.planes = planes_out
    bytype.rawdata = rawdata_out
    return "Passed"

def bystatus(planes,altitude,rawda,asphalt = "activated", airport = "EDFM"):
    if airport == "EDFM": #Coordinates of the start field, used to exclude starting gliders. Need to be specified for each airport.
        x1 = 49.47651
        x2 = 49.47299
        y1 = 8.520801
        y2 = 8.510299
    else:
        return "Error, the airport given is not known. Please contact the development."

    planes_out = []
    altitude_out = []
    for i in range(0,len(rawda)):
        if altitude[i][1] == "Muss landen":                                                                                      #If the aircaft is low,
            if float(rawda[i][9]) < 1.1:                                                                                         #and it doesn't climb much,
                #if float(rawda[i][0]) < x1 and float(rawda[i][0]) > x2 and float(rawda[i][1]) < y1 and float(rawda[i][1]) > y2:  #and its not inside the landing field: Its safe to say it is landing
                    #if asphalt == "activated":                                                                                   #except for one case: A motorglider starting from 09/27 (low climb rate)
                planes_out.append(planes[i])
                altitude_out.append(altitude[i])
                    #else:
                    #    return "Error, this module isn't accesible yet (filter.bystatus, option asphalt)"                        #No idea on how to solve that

    bystatus.planes = planes_out
    bystatus.altitude = altitude_out
    return "Passed"
