from GA.output import data                  #Import the data function from GA.output
ip = input()                                #Receiving needed arguments. Example: "Muss landen,03".
if ip[:11] == "Steht      ":                #Verify first argument
    ...
elif ip[:11] == "Muss landen":
    ...
elif ip[:11] == "Platzrunde ":
    ...
elif ip[:11] == "Frei       ":
    ...
else:
    print("Supplyerror. First argument is unknown.")
    exit()

try:                                        #Verify second argument
    x = int(ip[13:15])
except:
    print("Supplyerror. Second argument is unknown.")
    exit()

if int(ip[13:15]) == 0:
    print("Supplyerror. Number 0 is not possible.")
    exit()

trd = str(ip[:11].strip())
result = data("SMALL","all",trd)  #Call function with small output and all filters, apply category
ex = data.exitcode
if ex == "Passed":                          #Make sure everything went correctly
    if result == []:
        print("     Keiner da!")            #Prevent empty output
    else:
        output = ""
        for i in range(0,int(ip[13:15])-1): #Build output with 3 lines in total,
            try:
                output = output + "     " + result[i] + "%s\n"
            except:
                output = output + "%s\n"
        try:
            output = output + "     " + result[i+1]
        except:
            output = output
        print(output)
else:
    print("     " + ex)
