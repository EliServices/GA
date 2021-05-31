#To understand this script, you need to know:
#  - Basic SQL syntax

#This is the core of the program

#This function stops everything
def clean(db,log):
    db.disconnect()                                                      #Disconnect from MySQL
    log.close()                                                          #Close logfile


#This function initalizes and starts the data collection process
def collect(configpath,exitpath,logpath=""):
    import os
    import sys
    from time import sleep, ctime as ct, perf_counter as ts
    from datetime import date

    logpath = configpath
    log = open(logpath + "/ga.log", "a")

    try:                                                                   #The code tries to import the other .py scripts
        from .load import load                                             #load.py performs the initialization
        from .data import data                                             #data.py performs the http request and the data converting
        from .utils import fixes                                           #utils.py contains bugfixes, for further information look at utils.py
    except:
        log.write(ct().split()[3] + " GA: Missing required moduls.\n")     #Program can't be executed without those scripts
        sys.exit()

    try:
        t_load = ts()
        config=load(configpath)                                            #Calling load() (look at load.py to understand what it does)
        url=config[0]                                                      #This is the url for the http request
        db=load.db                                                         #We need to do this to save the object

        if config[1] == "console":                                         #Redirect output to console
            out = sys.stderr
        elif config[1] == "logfile":                                       #Redirect output to logfile
            out = log

        if config[1] != "silent": out.write(ct().split()[3] + " EliServices Ground Assistant Library started.\nLoading done in: " + str(round(ts() - t_load)) + "sec.\n\n")

    except:
        log.write(ct().split()[3] + " GA: Failed to call load().\n")       #Without url or db object we can't continue
        sys.exit()


    count = 0
    stat = 0
    actwrite = []
    fix = fixes(["empty"])
    dbc = db.cursor()                                                      #MySQL cursor() object
    t_before = ts()                                                        #Timestamp to measure the runtime

    while os.path.isfile(exitpath) == False:                               #We do this again and again until an event happens
        count += 1                                                         #Count the loops for statistics
        t_one = ts()                                                       #First timestamp

        try:
            aircrafts=data(sys,ts,db,url)                                  #Calling data() (look at data.py to understand what it does)
        except:
            out.write(ct().split()[3] + " GA: Failed to call data().\n")   #Abort if the data() function crashes
            nonsensetotriggerexcept                                        #Because this try/except is in another try/except, clean() wouldn't stop the program


        for i in range(0, len(aircrafts)):                                 #Every position in aircrafts contains a list
            doubled = fix.isin(aircrafts[i])                               #This is a bugfix that prevents data from beeing inserted twice
            if doubled:                                                    #If it returns True, the data is already there
                stat += 1

            else:
                x = {"INSERT INTO " +                                      #This is the MySQL-comand that inserts our data in the database
                     str(date.today()).replace("-","_") +
                     " VALUES (" +
                     "\"" + aircrafts[i][5] + "\"," +                      #"\"" is just a masked " that is needed because SQL wants a string to be in "
                     "\"" + aircrafts[i][11] + "\"," +
                     "\"" + aircrafts[i][12] + "\"," +
                     "\"" + aircrafts[i][10] + "\"," +
                     "\"" + aircrafts[i][2] + "\"," +
                     "\"" + aircrafts[i][3] + "\"," +
                     aircrafts[i][0] + "," +                               #No strings, no masked "
                     aircrafts[i][1] + "," +
                     aircrafts[i][8] + "," +
                     aircrafts[i][4] + "," +
                     aircrafts[i][9] + ");"}

                content = (''.join(list(x)))                               #Converts 2D list in string
                dbc.execute(content)                                       #Execute SQL command content[i]
                actwrite.append(aircrafts[i])

        if stat < len(aircrafts): wrote = "\nWe wrote new data:\n" + str(actwrite) + "\n"
        else: wrote = "All data is already in the database.\n"
        actwrite = []                                                      #Clean
        stat = 0
        db.commit()                                                        #Save changes
        fix = fixes(aircrafts)                                             #Re-initialize the fix for doubles

        if config[1] != "silent":                                          #Debug output
            usedtime = round(ts() - t_one,2)                               #Time needed
            time0 = "Done in " + str(usedtime) + "sec.\n"
            time1 = "Initalizing took " + str(data.time[0]) + "sec.\n"
            time2 = "Sending the request took " + str(data.time[1]) + "sec.\n"
            time3 = "Processing the request took " + str(data.time[2]) + "sec.\n"
            output = time0 + time1+ time2 + time3 + wrote + "Waiting for " + str(config[2]) + "sec.\n\n\n"
            out.write(ct().split()[3] + ":\n" + output)

        sleep(int(config[2]))

    if config[1] != "silent": out.write(ct().split()[3] + " EliServices Ground Assistant Library exited.\n")
    clean(db,log)
    return [count, ts() - t_before]

def version():
    from .load import version as l
    from .data import version as d
    from .utils import version as u
    lr = l()
    dr = d()
    ur = u()
    return "EliServices GA utility main.py at version 1.1\n" + lr + dr + ur
