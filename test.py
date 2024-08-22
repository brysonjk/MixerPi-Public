import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)

#ads.gain = 1

gains = (2 / 3, 1, 2, 4, 8, 16)
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

while True:
    ads.gain = gains[0]
    print("{:5} {:5.3f}".format(chan1.value, chan1.voltage), end="")
    for gain in gains[1:]:
        ads.gain = gain
        print(" | {:5} {:5.3f}".format(chan1.value, chan1.voltage), end="")
    print()
    time.sleep(1)




#    print(f"output1: {chan1.voltage}V")
#    print(f"output2: {chan2.voltage}V")
#    time.sleep(1)

