#This is the Ground Assistant (GA) system. It assembles the GA library functions in correct order.

def data(mode = "SMALL",sieve = "all",part = "",typeforsmall = "(Moto-) Glider  "):
    #We start by collecting relevant informations from local GASettings.eli
    #infofile = open("GASettings.eli", "r")
    #file = []
    #for zeile in infofile:
    #    x = zeile.strip
    #    if x[:1] != "#":
    #        file.append(x)
    #infofile.close()

    notice = ["Further notes:"]
    RUNMODES = ["DEBUG","SMALL","BIG","EXPERT"]
    RUNMODE = mode
    #First, we will import all the modules needed
    from . import settings
    from . import ognrequest
    from . import handlexml
    from . import filter

    #Next, we will create the url of our request:
    url = ognrequest.makeurl(settings.getvar())

    #Now we send the request and extract the data:
    reply = ognrequest.getxml(url)
    if str(reply) == "<Response [404]>":
        data.exitcode = "Error, url: " + url + " returned 404."
        return "Error, server is unavailable (output.data)"

    else:
        if RUNMODE == "DEBUG":
            param = "true"
        else:
            param = "false"
        aircrafts = ognrequest.trimxml(reply,param)

        #Next, we will further cut the data strings:
        rawdata = handlexml.extract(aircrafts)

        #Now its time to filter and organise:
        if sieve == "all":
            sorted = filter.bubblesort(rawdata) #Puts rawdata elements in ascending order (sorted by altitude)
            rawdata = sorted
            filtered = filter.extract_position(rawdata) #Deletes aircrafts that are too far away to be relevant
            rawdata = filtered
            data.sieve = "all"
        elif sieve == "bubbleonly":
            sorted = filter.bubblesort(rawdata) #Puts rawdata elements in ascending order (sorted by altitude)
            rawdata = sorted
            data.sieve = "bubbleonly"
        else:
            data.exitcode = "Error, unknown filter argument."
            data.sieve = "error"
            return ""

        #Now, we get our own coordinates in a secondary list:
        #coordinates = handlexml.conco(rawdata)                    !Currently not used!

        #Next, we find out which kind of aircraft we have:
        aircrafttype = handlexml.plane_type(rawdata)

        #Now, we look at the altitude:
        altitude = handlexml.altitude_info(rawdata)    #altitude[i][0] = alt AGL in m, [i][1] = status

        #This recognizes known gliders:
        planes = handlexml.plane_recognition(rawdata)  #planes[i][0] = Short sign (3 characters), [i][1] = sign (11 char.), [i][2] = Device-ID (6 char.)

        #We have now everything we need, its time to put things together, so that our target can read it.
        data.exitcode = "Passed"
        data.notice = notice

        if RUNMODE == "BIG":                                                                        #Return for further use of the data or bigger screens
            big = []
            big.append("Aircraft          Short  CallSign     Height AGL  Status       Device-ID")
            for i in range(0,len(rawdata)):
                big.append(aircrafttype[i] + "  " + planes[i][0] + "   " + planes[i][1] + "  " + altitude[i][0] + "     " + altitude[i][1] + "  " + planes[i][2])

            return big

        elif RUNMODE == "SMALL":                                                                    #Return for smaller displays
            onlytype = filter.bytype(typeforsmall,aircrafttype,planes,altitude,rawdata)
            planes = filter.bytype.planes
            altitude = filter.bytype.altitude
            rawdata = filter.bytype.rawdata
            #data.smalltest1 = [planes, altitude, rawdata]     #Debug option

            #This is needed for the bashsupply.py usecase
            small = []
            if part == "Steht":
                for i in range(0, len(rawdata)):
                    if altitude[i][1] == "Steht      ":
                        small.append(planes[i][0] + " " + planes[i][1] + " " + altitude[i][0])
            elif part == "Muss landen":
                antistart = filter.bystatus(planes,altitude,rawdata)
                data.test = [filter.bystatus.planes, filter.bystatus.altitude]
                for i in range(0, len(filter.bystatus.planes)):
                    if filter.bystatus.altitude[i][1] == "Muss landen":
                        small.append(filter.bystatus.planes[i][0] + " " + filter.bystatus.planes[i][1] + " " + filter.bystatus.altitude[i][0])
            elif part == "Platzrunde":
                for i in range(0, len(rawdata)):
                    if altitude[i][1] == "Platzrunde ":
                        small.append(planes[i][0] + " " + planes[i][1] + " " + altitude[i][0])
            elif part == "Frei":
                for i in range(0, len(rawdata)):
                    if altitude[i][1] == "Frei       ":
                        small.append(planes[i][0] + " " + planes[i][1] + " " + altitude[i][0])
            else:
                notice.append("Part argument was unknown.")
                for i in range(0,len(rawdata)):
                    small.append(planes[i][0] + " " + planes[i][1] + " " + altitude[i][0])
                    small2 = "Hii"
            return small

        #Getting to the end of the program, we need to specify what we want to give back:
        if RUNMODE == "DEBUG":
            data.inbound = mode + ", " + sieve + ", " + part + ", " + middlereturn
            data.aircrafttype = aircrafttype
            data.altitude = altitude
            data.planes = planes
            data.big = big
            data.all = sorted
            data.url = url
            return rawdata
        elif RUNMODE == "EXPERT":
            return big
        else:
            data.exitcode = "Error, unknown / unspecified runmode."
            return ""
