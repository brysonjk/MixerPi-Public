#!/usr/bin/python3

import time, os
from O2SENSOR_old import *

while True:
   O2_S0 = round(chan0.value / FAC_S0,1)
   O2_S1 = round(chan1.value / FAC_S1,1)
   S0 = round(chan0.value * 0.00781274,1)
   S1 = round(chan1.value * 0.00781274,1)
#   S2 = round(adc(2, gain=16) * 0.00781274,1)
#   S3 = round(adc(3, gain=16) * 0.00781274,1)
   os.system('clear')
   print(" ", "S0:", S0,"mV\tChan_val: ", chan0.value, "\tO2_S0: ", O2_S0,'%\t', FAC_S0)
   print(" ")
#   print(" ", "S1:", S1,"mV""		", O2_S1,'%',"	", FAC_S1)
#   print(" ")
#   print(" ", "S2:", S2,"mV")
#   print(" ")
#   print(" ", "S3:", S3,"mV")
   time.sleep(0.1)
