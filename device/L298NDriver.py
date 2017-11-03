#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO 

class L298N(object):
  def __init__(self, pins, pwapins, frequency):
    self.pin_pwm_a = pwapins[0]
    self.pin_pwm_b = pwapins[1]
    self.pin_input_1 = pins[0]
    self.pin_input_2 = pins[1]
    self.pin_input_3 = pins[2]
    self.pin_input_4 = pins[3]
    self.frequency_a = frequency[0]
    self.frequency_b = frequency[1]
  
  def init_gpio(self):
    GPIO.setup(self.pin_input_1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_input_2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_input_3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_input_4, GPIO.OUT, initial=GPIO.LOW)
  
  def init_pwm(self):
    GPIO.setup(self.pin_pwm_a, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_pwm_b, GPIO.OUT, initial=GPIO.LOW)
    self.pwm_a = GPIO.PWM(self.pin_pwm_a, self.frequency_a)
    self.pwm_a.start(0)
    self.pwm_b = GPIO.PWM(self.pin_pwm_b, self.frequency_b)
    self.pwm_b.start(0)
  
  def out_a_start_up(self, dutycycle):
    GPIO.output(self.pin_input_1, GPIO.LOW)
    GPIO.output(self.pin_input_2, GPIO.HIGH)
    self.pwm_a.ChangeDutyCycle(dutycycle)
  
  def out_a_reverse(self, dutycycle):
    GPIO.output(self.pin_input_1, GPIO.HIGH)
    GPIO.output(self.pin_input_2, GPIO.LOW)
    self.pwm_a.ChangeDutyCycle(dutycycle)
  
  def out_b_start_up(self, dutycycle):
    GPIO.output(self.pin_input_3, GPIO.LOW)
    GPIO.output(self.pin_input_4, GPIO.HIGH)
    self.pwm_b.ChangeDutyCycle(dutycycle)
  
  def out_b_reverse(self, dutycycle):
    GPIO.output(self.pin_input_3, GPIO.HIGH)
    GPIO.output(self.pin_input_4, GPIO.LOW)
    self.pwm_b.ChangeDutyCycle(dutycycle)
  
  def out_a_stop(self):
    GPIO.output(self.pin_input_1, GPIO.LOW)
    GPIO.output(self.pin_input_2, GPIO.LOW)
    self.pwm_a.ChangeDutyCycle(0)
    
  def out_b_stop(self):
    GPIO.output(self.pin_input_3, GPIO.LOW)
    GPIO.output(self.pin_input_4, GPIO.LOW)
    self.pwm_b.ChangeDutyCycle(0)
  
