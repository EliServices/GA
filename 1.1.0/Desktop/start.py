#This is the daemon executer for Ground Assistant.

def version():
    from ground_assistant.main import version as m
    from stop import version as s
    mr = m()
    sr = s()
    return "Verions of EliServices GA:\nEliServices GA utility start.py at version 1.0\n" + sr + mr

if __name__ == '__main__':
    import os,sys,ground_assistant
    from time import ctime

    path = os.path.abspath(".") + "/"                                                                                   #Our local path
    logpath = path                                                                                                      #path where the logfile is at

    try:
        os.remove(path + "exit")                                                                                        #This is GAs exit-event, as soon as this file appears, it will stop
    except:
        pass

    exe = ground_assistant.collect(path, path + "exit", logpath)                                                        #Execute program

    if type(exe) != list:                                                                                               #If there is no list returned, something went wrong
        out = open(logpath + "ga.log","a")                                                                              #Open logfile
        out.write(str(ctime().split()[3]) + " GA Daemon: Exit 1:\n")                                                    #So we mark that in the logfile
        out.close()                                                                                                     #Close logfile
        sys.exit(1)                                                                                                     #Exit with an error

    t_name = "sec."                                                                                                     #This is just to make the end message nicer
    if exe[1] > 120:                                                                                                    #More than 120 seconds...
        exe[1] = exe[1] / 60                                                                                            #will be shown as minutes
        t_name = "min."
        if exe[1] > 120:                                                                                                #More than 120 minutes...
            exe[1] = exe[1] / 60                                                                                        #will be shown as hours
            t_name = "h."
    t = str(round(exe[1],2)) + t_name                                                                                   #Round & put together

    out = open(logpath + "ga.log","a")                                                                                  #Open logfile
    out.write(ctime().split()[3] + " GA Daemon: Executed " + str(exe[0]) + " loops in " + t + "\n")                     #End message
    out.close()                                                                                                         #Close logfile
    sys.exit()
