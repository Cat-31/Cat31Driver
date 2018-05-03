#! /usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import TB6612FNG as tb6612fng

GPIO.setmode(GPIO.BCM)
config = {'stby': 20, 'ch_a': {'pins': [6, 13], 'pwm': {'pin': 5, 'frq': 1}},
          'ch_b': {'pins': [19, 26], 'pwm': {'pin': 21, 'frq': 1}}}
print(config)

motor = tb6612fng.TB6612FNG(config)
time.sleep(1)

motor.ch_a_start_up(50)
time.sleep(3)

motor.ch_a_reverse(80)
time.sleep(3)

motor.ch_b_start_up(50)
time.sleep(3)

motor.ch_b_reverse(50)
time.sleep(3)

motor.ch_a_stop()
motor.ch_b_stop()
GPIO.cleanup()
