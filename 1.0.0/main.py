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

        if config[1] != "silent": out.write(ct().split()[3] + " EliServices Ground Assistant Daemon started.\nLoading done in: " + str(round(ts() - t_load)) + "sec.\n\n")

    except:
        log.write(ct().split()[3] + " GA: Failed to call load().\n")       #Without url or db object we can't continue
        sys.exit()


    count = 0
    last = []
    dbc = db.cursor()                                                      #MySQL cursor() object
    t_before = ts()                                                        #Timestamp to measure the runtime
    while os.path.isfile(exitpath) == False:                                #We do this again and again until an event happens
        try:
            count = count + 1                                              #Count the loops for statistics
            t_one = ts()                                                   #First timestamp

            try:
                aircrafts=data(sys,ts,db,url)                              #Calling data() (look at data.py to understand what it does)
            except:
                out.write(ct().split()[3] + " GA: Failed to call data().\n") #Abort if the data() function crashes
                nonsensetotriggerexcept                                    #Because this try/except is in another try/except, clean() wouldn't stop the program

            wrote = "didn't write new data."
            if aircrafts != last:                                          #In case we are faster than the OGN-Network, this safes resources
                content = []
                for i in range(0, len(aircrafts)):                         #Every position in aircrafts contains a list
                    x = {"INSERT INTO " +
                         str(date.today()).replace("-","_") +
                         " VALUES (" +
                         "\"" + aircrafts[i][5] + "\"," +
                         "\"" + aircrafts[i][11] + "\"," +
                         "\"" + aircrafts[i][12] + "\"," +
                         "\"" + aircrafts[i][10] + "\"," +
                         "\"" + aircrafts[i][2] + "\"," +
                         "\"" + aircrafts[i][3] + "\"," +
                         aircrafts[i][0] + "," +
                         aircrafts[i][1] + "," +
                         aircrafts[i][8] + "," +
                         aircrafts[i][4] + "," +
                         aircrafts[i][9] + ");"}

                    content.append(''.join(list(x)))                       #Converts 2D list in string
                    dbc.execute(content[i])                                #Execute SQL command content[i]
                wrote = "wrote new data:\n" + str(aircrafts)
                db.commit()                                                #Save changes

            last = aircrafts                                               #Save aircrafts

            if config[1] != "silent":
                usedtime = round(ts() - t_one,2)                           #Time needed
                time0 = "Done in " + str(usedtime) + "sec.\n"
                time1 = "Initalizing took " + str(data.time[0]) + "sec.\n"
                time2 = "Sending the request took " + str(data.time[1]) + "sec.\n"
                time3 = "Processing the request took " + str(data.time[2]) + "sec.\n"
                output = time0 + time1+ time2 + time3 + "\nWe " + wrote + "\n\nWaiting for " + str(config[2]) + "sec.\n\n\n"
                out.write(ct().split()[3] + ":\n" + output)
        except:
            if config[1] != "silent": out.write(ct().split()[3] + " GA: Failed to process and write data.\n")
            clean(db,log)
            return [count, ts() - t_before]

        sleep(int(config[2]))

    if config[1] != "silent": out.write(ct().split()[3] + " EliServices Ground Assistant Daemon exited.\n")
    clean(db,log)
    return [count, ts() - t_before]

def version():
    from load import version as l
    from data import version as d
    lr = l()
    dr = d()
    return "EliServices GA utility main.py at version 1.0\n" + lr + dr
