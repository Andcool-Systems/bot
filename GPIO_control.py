import os
import time

def pinMode(_pin, _dir):
	os.system("echo "+ str(_pin) +" > /sys/class/gpio/export")
	time.sleep(2)
	os.system("echo " + str(_dir) + " > /sys/class/gpio/gpio" + str(_pin) + "/direction")
	time.sleep(2)

def digitalWrite(_pin, _val):
	os.system("echo " + str(_val) + " > /sys/class/gpio/gpio" + str(_pin) + "/value")
