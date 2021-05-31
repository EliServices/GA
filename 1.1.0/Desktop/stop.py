#This stops the GA daemon

def version():
    return "EliServices GA utility stop.py at version 1.0\n"

if __name__ == '__main__':
    from os import path,remove
    from time import sleep

    file = open(path.abspath(".") + "/exit","a")  #Create stop file
    file.write("stop")
    file.close
    sleep(5)                                      #Wait to make sure it stopped
    remove(path.abspath(".") + "/exit")           #Remove stop file
