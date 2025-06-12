#!.venv/bin/python3
# -*- coding: utf-8 -*-

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from simple_pid import PID
import board
import busio
import time
import threading

# Constant
MULTIPLIER = 0.0078125
CALIBRATION_DELAY = 10  # Delay in seconds during calibration
EMA_UPDATE_INTERVAL = 0.01  # Interval for EMA updates
PID_MIN = 0  # Minimum PID output
PID_MAX = 255  # Maximum PID output

# variables
targetOxygen = 0.0

# I2C and ADC setup
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)

# Calibration state
calibrated0 = False
calValue0 = 0.0

# Exponential Moving Average (EMA) class
class EMA:
    def __init__(self, k):
        self.k = k
        self.state = 0
        self.half = 1 << (k - 1)
        self.output = 0.0

    def update(self, input_value):
        """Update the EMA with a new input value."""
        self.state += input_value
        self.output = (self.state + self.half) >> self.k
        self.state -= self.output
        return self.output

    def getEmaValue(self):
        """Get the current EMA value."""
        return self.output

# Function to run EMA updates in a thread
def ema_thread(ema_instance, input_source, interval=EMA_UPDATE_INTERVAL):
    """Continuously update the EMA instance with values from the input source."""
    while True:
        input_value = input_source()
        ema_instance.update(input_value)
        time.sleep(interval)

# Calibration function
def calibrate(ema):
    """Calibrate the EMA by averaging sensor data over a period."""
    print("Starting calibration...")
    for _ in range(CALIBRATION_DELAY):  # Simulate 10 seconds of calibration
        time.sleep(1)
    print("Calibration complete.")
    return ema.getEmaValue()

# Sensor data functions
def get_chan0_data():
    """Get data from channel 0."""
    ads.gain = 16
    return chan0.value

def get_chan1_data():
    """Get data from channel 1."""
    ads.gain = 16
    return chan1.value

# create PID function
def initializePID(Kp, Ki, Kd, sp=targetOxygen):
    pid = PID(Kp,Ki,Kd,sp)
    pid.output_limits = (PID_MIN, PID_MAX)  # Limit PID Moutput to a range
    return pid

# Target Setpoint functions
def setTargetOxygen(target):
    targetOxygen = target

def getTargetOxyget():
    return targetOxygen

def pid_thread(pid, ema_instance, cal_value, interval=0.01):
    """Continuously calculate PID output based on EMA values."""
    while True:
        if cal_value != 0:  # Ensure calibration is complete
            ema_value = ema_instance.getEmaValue()
            oxygen_reading = (ema_value / cal_value) * 20.9
            
            #Calculate PID Output
            pid_output = pid(oxygen_reading)
            return pid_output
        else:
            print(f"cal_value = {cal_value}")
            print("Channel 0 not calibrated.")

   

# Main function
def main():
    # Create an EMA instance for channel 0
    ema0 = EMA(k=4)

    # Start the EMA thread for channel 0
    threading.Thread(target=ema_thread, args=(ema0, get_chan0_data), daemon=True).start()


    # Calibrate channel 0
    global calibrated0, calValue0
    if not calibrated0:
        calValue0 = calibrate(ema0)
        calibrated0 = calValue0 != 0

    # Initialize PID controller
    pid = initializePID(1.0, 5.0, 0.1, targetOxygen)

    # Start the PID thread
    threading.Thread(target=pid_thread, args=(pid, ema0, calValue0), daemon=True).start()
    loop=0
    # Main loop to display sensor data and calculate PID output
    while True:
        
        if calibrated0:

            ema_value = ema0.getEmaValue()
            oxygen_reading = (ema_value / calValue0) * 20.9

            # Calculate PID output
            pid_output = pid(oxygen_reading)

            # Print sensor data and PID output
            print(f"Updated EMA value: {ema_value}")
            print(f"Calibration Value: {calValue0}")
            print(f"Oxygen Reading: {oxygen_reading:.1f}%")
            print(f"PID Output: {pid_output:.2f}")
            print(f"Loop Value: {loop}")
            loop+=1
            if (loop == 5):
                pid.setpoint = 32
            if (loop ==10):
                pid.setpoint = 18
        else:
            print("Channel 0 not calibrated.")
        time.sleep(1)

if __name__ == "__main__":
    main()