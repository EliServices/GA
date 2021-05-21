#Functions for http requests to the ogn server, v.1.

def makeurl(setti): #Generates an http url
    ogn = "http://live.glidernet.org" #Internet adress of the Server
    lxml = "/lxml.php?"               #Type of request that is send
    livexml = "/livexml1.php?"
    data = "/dataxml.php?"

    a = setti[0]
    b = setti[1]
    c = setti[2]
    d = setti[3]
    e = setti[4]
    filter = "a=" + a + "&b=" + b + "&c=" + c + "&d=" + d + "&e=" + e #Assembles filter

    types = ["lxml", "livexml", "data"] #Finds out which type of request is needed (position 5 in settings)
    a = types.index(setti[5])

    b = 0
    if a == b:
        url = ogn + lxml + filter #Assembels url
    b = 1
    if a == b:
        url = ogn + livexml + filter #Assembels url
    b = 2
    if a == b:
        url = ogn + data + filter #Assembels url
    return url
    #print("Made url.")

def getxml(u):
    import requests
    #print("Sending get request to: " + u + "\n")
    reply = requests.get(u)
    #print("Answer: \n" + rely.text)
    return reply

def trimxml(repl, debug = "false"):
    if debug == "false":
        input = repl.text
    else:
        input = "<markers>\n<m a=\"49.479802,8.526881,DK1,D-IDK1,400,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"50.000000,7.000000,DK2,D-IDK2,400,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"49.473500,8.520000,DK3,D-IDK3,400,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"49.473910,8.509852,DK4,D-IDK4,150,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"49.479802,8.526881,DK5,D-IDK5,400,XX:XX:XX,36301,X,Speed,0.0,A,Receiver,Device,xxxxxx\"/>\n<m a=\"49.479802,8.526881,DK6,D-IDK6,150,XX:XX:XX,36301,X,Speed,0.0,A,Receiver,Device,xxxxxx\"/>\n<m a=\"49.479802,8.526881,DK7,D-IDK7,95,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"49.479802,8.526881,DK8,D-IDK8,4000,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n<m a=\"49.479802,8.526881,DK9,D-IDK9,150,XX:XX:XX,36301,X,Speed,0.0,1,Receiver,Device,xxxxxx\"/>\n</markers>"

    xml = input.split("\n")
    begin = xml.index("<markers>") + 1
    end = xml.index("</markers>") - 1
    found = end - begin + 1 #if begin = 2 and end = 4 then found = 4 - 2 = 2 but there are 3 (2,3,4)
    #print(str(found) + " aircrafts found")

    aircrafts = []
    for i in range(begin, end + 1):
        aircrafts.append(xml[i])

    for i in range(len(aircrafts)):
        aircrafts[i] = aircrafts[i].lstrip("<m a=\"")
        aircrafts[i] = aircrafts[i].rstrip("\"/>")

    return aircrafts
