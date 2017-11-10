#! /usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import SteeringEngineDriver as sedriver

GPIO.setmode(GPIO.BCM)
config={'pin':21,'angle':90}
se =  sedriver.SteeringEngine(config)

time.sleep(2)

se.move_to(30)
GPIO.cleanup()

