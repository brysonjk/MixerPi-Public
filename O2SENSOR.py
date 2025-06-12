#!.venv/bin/python3
# -*- coding: utf-8 -*-

#import pandas as pd
#import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio

O2_COUNT = 6
FAC_COUNT = 50
FAC_S0 = 0.0
FAC_S1 = 0.0

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)



def sensor_env():
        global FAC_S0
        global FAC_S1

        FAC_S0 = 0.0
        FAC_S1 = 0.0

        for x in range (1,FAC_COUNT):
               ads.gain = 16
               FAC_S0 += chan0.value
        FAC_S0 = (FAC_S0 / FAC_COUNT / 20.9) 
        
        for x in range (1,FAC_COUNT):
                ads.gain = 16
                FAC_S1 += chan1.value
        FAC_S1 = (FAC_S1 / FAC_COUNT / 20.9)

sensor_env()

""" def ema(s, n):

    returns an n period exponential moving average for
    the time series s

    s is a list ordered from oldest (index 0) to most
    recent (index -1)
    n is an integer

    returns a numeric array of the exponential
    moving average

    s = array(s)
    ema = []
    j = 1

    #get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    #EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(( (s[n] - sma) * multiplier) + sma)

    #now calculate the rest of the values
    for i in s[n+1:]:
        tmp = ( (i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)

    return ema """

""" def ExpMovingAverage (values, window):
        weights = np.exp(np.linspace(-1.,0.,window))
        weights /= weights.sum()
        ema = np.convolve(values,weights)[:len(values)]
        ema[:window]=ema[window]
        return ema """

def calibrate():
        for x in range (1,FAC_COUNT):
                ads.gain = 16
                FAC_S0 += chan0.value
        FAC_S0 = (FAC_S0 / FAC_COUNT / 20.9) 
        for x in range (1,FAC_COUNT):
                ads.gain = 16
                FAC_S1 += chan1.value
        FAC_S1 = (FAC_S1 / FAC_COUNT / 20.9)

def get_O2_S0():
        O2_S0_INT = O2_COUNT
        O2_S0 = 0
        for x in range (0,O2_COUNT):
               ads.gain = 16
               O2_S0 += chan0.value
        O2_S0 = (O2_S0 / O2_COUNT / FAC_S0)
        return (O2_S0)

def get_O2_S1():
        O2_S1_INT = O2_COUNT
        O2_S1 = 0
        for x in range (0,O2_COUNT):
               ads.gain = 16
               O2_S1 += chan1.value
        O2_S1 = (O2_S1 / O2_COUNT / FAC_S1)
        return (O2_S1)


