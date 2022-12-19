from os import popen
from sys import argv, exit, stdout
from getopt import getopt
from time import sleep
try:
    os.system("sudo pip install aioschedule")
except Exception:
    pass
def readTemp():
    try:
        file = open("/sys/class/thermal/thermal_zone0/temp", "r")
        temp = int(file.read().replace("\n", ""))
        file.close()
        return(temp)
    except:
        pass


def convertTemp(temp):
    if temp > 200:
        return (temp / 1000)
    return(temp)



def formatTemp():
    temp = convertTemp(readTemp())

    return(temp)


def printTemp():
    try:
        return formatTemp()
    except KeyboardInterrupt:
        print("")



