
#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import atexit
import HCSR04 as hcsr04

atexit.register(GPIO.cleanup)

GPIO.setmode(GPIO.BCM)
config={'pins':{'T':23,'R':24}, 'voice_speed':340}
print(config)

ud  = hcsr04.HCSR04(config)

while True:
  print(ud.get_distance())
  time.sleep(2)



