#To understand this script, you need to know:
#  - Basic SQL syntax
#  - Syntax of live.glidernet.org

#This script is responsible for receiving the xml from the ogn-server
#and organizing the database "ogn" (=> Preparing everything)

#Make a new table:
def organize(sys,ts,db): #sys = sys module, ts = time.perf_counter object, db = MySQL object from load.py
    from datetime import date

    #Create today's table
    try:
        t_one = ts()                                          #First timestamp
        dbc = db.cursor()                                     #Create cursor() object to acces MySQL
        x = {"CREATE TABLE IF NOT EXISTS " +                  #x is the SQL command to create a table
             str(date.today()).replace("-","_") +             #where the name is todays date
             " ( time TIME," +                                #First row is a timestamp,
             " receiver VARCHAR(255)," +                      #second the receiver,
             " device_id VARCHAR(6)," +                       #FLARM ID,
             " type VARCHAR(20)," +                           #type of aircraft,
             " short VARCHAR(5)," +                           #Few letters to quickly identify the aircraft,
             " callsign VARCHAR(10)," +                       #official callsign,
             " north DOUBLE(180,7)," +                        #coordinates north,
             " east DOUBLE(180,7)," +                         #coordinates south,
             " speed INT(255)," +                             #speed,
             " msl INT(255)," +                               #hight above sealevel (MSL),
             " climbrate FLOAT(10));"}                        #and the climbrate

        dbc.execute(''.join(list(x)))                         #Execute the command
        row = list(dbc.fetchall())                            #Read SQL's reaction (=> 2D list)
        row = [x for sublist in row for x in sublist]         #This makes the 2D list row 1D

        t_two = ts()                                          #Second timestamp
        return round(t_two - t_one,2)                         #Returns the time it needed

    except:
        sys.stderr.write("GA: Failed to create today's table.\n") #Error code
        return None                                               #Return time needed


#Get the xml:
def getxml(sys,ts,url): #sys = sys module, ts = time.perf_counter object, url from load.py
    import requests
    from operator import itemgetter

    #Send the request and find the beginning and the end of the actual data
    try:
        t_one = ts()                                          #First timestamp
        reply = requests.get(url)                             #Sending http-request via requests lib
        inp = reply.text                                      #reply would be the status of the request
        t_one = round(ts() - t_one,2)                         #Time needed

    except:
        sys.stderr.write("GA: Failed to send request.\n")     #Error Code
        getxml.time = [None,None]                             #Make time available
        return []                                             #to make sure the next instance doesn't crash


    #Seperate the data from the rest and sort it by time
    try:
        t_two = ts()                                          #Second timestamp
        xml = inp.split("\n")                                 #Create a list, each position containing one line
        begin = xml.index("<markers>") + 1                    #Identify the first line containing data
        end = xml.index("</markers>") - 1                     #Identify the last line containing data

        aircrafts = []
        for i in range(begin, end+1):                         #For all lines containing data:
            a = xml[i].lstrip("<m a=\"")                      #    Cut off the start flags of the HTML
            a = a.rstrip("\"/>")                              #    Cut off the end flags of the HTML
            aircrafts.append(a.split(","))                    #    Write the data, which is now clean, into a list
                                                              #    This list is 2D, because HTML line is splitted
                                                              #    in a list, which is the assigned to the list
        aircrafts = sorted(aircrafts,key=itemgetter(5))       #Sort list items (lists ) by the 5. pos. of each list

        t_two = round(ts() - t_two,2)                         #Time needed
        getxml.time1 = t_one                                  #Make time available
        getxml.time2 = t_two
        return aircrafts                                      #Returning the results

    except:
        sys.stderr.write("GA: Failed to process request.\n")  #Error Code
        getxml.time = [t_one,None]                            #Make time available
        return []                                             #Return empty list


#Call the functions above:
#Parameter explanation:
#    sys: simply the sys module
#    ts : time.pef_counter object
#    db : a MySQL-Connector object, which was prepared by ./load.py
#    url: a url (type string) genrated by ./load.py

def data(sys,ts,db,url): #The reason for this function is to keep main clean
    time0 = organize(sys,ts,db)                              #Call organize() (Returns its time)
    aircrafts = getxml(sys,ts,url)                           #Call getxml() (Returns aircrafts)
    data.time = [time0,getxml.time1,getxml.time2]            #Make times available
    return aircrafts                                         #return results

def version():
    return "EliServices GA utility data.py at version 1.1\n"
