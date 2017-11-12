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
    duty_cycle = 2.5 + 10*angle/180
    # 大角度转动 响应时间？
    for i in range(0,5,1):
        self.pwm.ChangeDutyCycle(duty_cycle) 
        time.sleep(0.02)                      
        self.pwm.ChangeDutyCycle(0)    
        
    self.pwm.ChangeDutyCycle(0)
    self.current_angle = angle


