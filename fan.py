import os
import time
import threading
from temp import printTemp
from GPIO_control import pinMode, digitalWrite
frenq = 10
pwm_deg = 20
frenq_lvl = ((1000 / 20) / 2) / 1000
fps = 0
lt_fps = 0
last_time = 0
temp_c = 0
temp_sum = 0
done = False
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
pinMode(228, "out")

def start():
    global pwm_deg
    global frenq
    global last_time
    global temp_c
    global temp_sum
    while True:
        temp1 = round(printTemp())
        if done == False:
            temp2 = round(printTemp())
            temp_sum += temp2
            temp_c += 1
            if temp_c == 500:
                temp1 = temp_sum / temp_c 

            
        if (time.time() - last_time) * 1000 > 1500:
            last_time = time.time()
            
            if temp1 <= 55:
                pwm_deg = 0
                digitalWrite(228, 0)
            if temp1 > 60:
                pwm_deg = 100
                digitalWrite(228, 1)
            """
            pwm_deg = map(temp1, 55, 65, 50, 100)
            pwm_deg = round(min(100, max(50, pwm_deg)))
            if temp1 <= 55:
                pwm_deg = 0
            
        #pwm_deg = 50
        
        print(temp1)
        if pwm_deg != 100 and pwm_deg != 0:
            os.system("echo 1 > /sys/class/gpio/gpio228/value")
            time.sleep((frenq_lvl / 100) * pwm_deg)
            os.system("echo 0 > /sys/class/gpio/gpio228/value")
            
            time.sleep((frenq_lvl / 100) * (100 - pwm_deg))
        if pwm_deg == 100:
            os.system("echo 1 > /sys/class/gpio/gpio228/value")

        if pwm_deg == 0:
            os.system("echo 0 > /sys/class/gpio/gpio228/value")
        """
  

th = threading.Thread(target=start)
th.start()

