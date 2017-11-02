#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(5, GPIO.OUT, initial=False)


GPIO.output(16, GPIO.HIGH)
GPIO.output(5, GPIO.HIGH)

GPIO.output(6,GPIO.LOW)
GPIO.output(13,GPIO.LOW)
GPIO.output(19,GPIO.LOW)
GPIO.output(26,GPIO.HIGH)
time.sleep(2)

GPIO.setup(5, GPIO.OUT, initial=False)
p = GPIO.PWM(5,1) 
p.start(50)
time.sleep(10)


GPIO.cleanup()
