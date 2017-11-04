#! /usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import L298NDriver as l298n

GPIO.setmode(GPIO.BCM)
config={'ch_a':{'pins':[6,13],'pwm':{'pin':5,'frq':0.5}},'ch_b':{'pins':[19,26],'pwm':{'pin':21,'frq':1}}}
print(config)

motor=l298n.L298N(config)
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

