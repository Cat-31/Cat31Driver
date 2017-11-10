#! /usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

class SteeringEngine(object):
  def __init__(self, config):
    GPIO.setup(config['pin'], GPIO.OUT, initial=GPIO.LOW)
    self.pwm = GPIO.PWM(config['pin'], 50)
    self.pwm.start(0)
    self.current_angle = config['angle']
    self.move_to(self.current_angle)

  def move_to(self, angle):
    step = (1 if angle >= self.current_angle else -1)
    # print(2.5 + 10 * self.current_angle/180)
    for i in range(self.current_angle, angle + step, step):
      self.pwm.ChangeDutyCycle(2.5 + 10 * i / 180)
      time.sleep(0.02)
      # print(i)
      # print(2.5 + 10 * i / 180)

    self.pwm.ChangeDutyCycle(0)
    self.current_angle = angle


