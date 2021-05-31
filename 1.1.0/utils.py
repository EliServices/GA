#To understand the following code you need to understand the problem:
#"aircrafts" is a two-dimensional list, with each position containing a list which contains the data of the plane.
#"aircrafts" is renewed by a given interval which isn't necessarily the same the data of the plane is renewed with.
#This means that "aircrafts" at t = 1 can contain the same data of plane X as at t = 2, so the data would be doubled.
#The code finds out if the data from plane X at t = 2 is the same as at t = 1, and if this is the case, it returns True.

class fixes:                                                                                            #Object fixes:
    def __init__(self,last=None,debug=False):                                                           #Initialize class fixes with the last aircrafts (var "last" in main.py)
        import sys
        self.last = last                                                                                #Initzialize variables
        self.flat = []                                                                                  #Is empty, will be filled with the first call of isin()

        self.debug = debug
        if debug == True:
            self.out = sys.stderr                                                                       #Optional debug output

    def isin(self,aircraft):                                                                            #Call fixes.isin() with the data of a single aircraft from aircrafts (list aircrafts[i] in main.py)
        if self.debug == True: self.out.write("Searchterm: " + str(aircraft) + "\n")
        short = aircraft[2]                                                                             #The 'name' of the aircraft
        ts = aircraft[5]                                                                                #The 'timestamp' of the aircraft

        if self.last:                                                                                   #If the self.last var cotains something (= main.py renewed its content)
            self.flat = [x for sublist in self.last for x in sublist]                                       #Self.flat is self.last without sublists (Converting 2D list into 1D list)
            self.lastsave = self.last                                                                       #Save self.last internal as self.lastsave
            self.last = []
            if self.debug == True: self.out.write("Renewed flat to: "  + str(self.flat) + "\n")

        if short in self.flat:                                                                          #If the 'name' of the aircraft is somewhere in self.last (=self.flat)
            if self.debug == True: self.out.write(short + " is in " + str(self.flat) + "\n")
            fpos = self.flat.index(short) + 1                                                               #Position in flat + 1 to avoid /0 errors, the 1 is removed a few lines later
            if self.debug == True: self.out.write("fpos: " + str(fpos) + "\n")

            lpos = (fpos / 14) + 0.5                                                                        #Position in the flatened list / Items in each sublist in last (+ 0.5 => always round up)
            lpos = int(round(lpos,0)) - 1                                                                   #Round and convert to int because the / operation probably made it a float
            if self.debug == True: self.out.write("lpos: " + str(lpos) + "\nResult: ")

            if ts == self.lastsave[lpos][5]:                                                                #Now that we know where our timestamp is in last, we can compare them
                if self.debug == True: self.out.write("True\n\n\n")
                return True                                                                                 #And if they are equal, the data is equal.
            else:
                if self.debug == True: self.out.write("False\n\n\n")
                return False
        else:                                                                                           #If it's not, then there is no data from plane X at t = 1, so nothing doubled at t = 2
            if self.debug == True: self.out.write(short + " isn't in " + str(self.flat) + "\nResult: False\n\n\n")
            return False

        return ret

    def test():
        pass

def version():
    return "EliServices GA utility utils.py at version 1.1"
