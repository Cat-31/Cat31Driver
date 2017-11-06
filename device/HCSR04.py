
#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time

class HCSR04(object):
  def __init__(self,config):
    self.pin_t = config['pins']['T']
    self.pin_r = config['pins']['R']
    self.voice_speed = config['voice_speed']

    GPIO.setup(self.pin_t, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_r, GPIO.IN)

  def trig(self, sec):
    GPIO.output(self.pin_t, GPIO.HIGH)
    time.sleep(sec)
    GPIO.output(self.pin_t, GPIO.LOW)

  def get_distance(self):
    self.trig(0.000015)
    while not GPIO.input(self.pin_r):
      pass
    t_start = time.time()

    while GPIO.input(self.pin_r):
      pass
    t_end = time.time()

    return (t_end - t_start)*self.voice_speed/2
