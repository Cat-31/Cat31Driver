#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO

class L298N(object):
  def __init__(self,config):
    if 'ch_a' in config:
      self.ch_a_input = config['ch_a']['pins']
      self.setup_gpio(self.ch_a_input,[GPIO.LOW, GPIO.LOW])

      if 'pwm' in config['ch_a']:
        pwm = config['ch_a']['pwm']
        GPIO.setup(pwm['pin'], GPIO.OUT, initial=False)
        self.pwm_a = GPIO.PWM(pwm['pin'],pwm['frq'])
        self.pwm_a.start(0)

    if 'ch_b' in config:
      self.ch_b_input = config['ch_b']['pins']
      self.setup_gpio(self.ch_b_input,[GPIO.LOW, GPIO.LOW])

      if 'pwm' in config['ch_b']:
        pwm = config['ch_b']['pwm']
        GPIO.setup(pwm['pin'], GPIO.OUT, initial=GPIO.LOW)
        self.pwm_b = GPIO.PWM(pwm['pin'],pwm['frq'])
        self.pwm_b.start(0)

  def ch_a_start_up(self, dutycycle):
    self.set_gpio(self.ch_a_input,[GPIO.LOW, GPIO.HIGH])
    self.pwm_a.ChangeDutyCycle(dutycycle)

  def ch_a_reverse(self, dutycycle):
    self.set_gpio(self.ch_a_input,[GPIO.HIGH, GPIO.LOW])
    self.pwm_a.ChangeDutyCycle(dutycycle)

  def ch_b_start_up(self, dutycycle):
    self.set_gpio(self.ch_b_input,[GPIO.LOW, GPIO.HIGH])
    self.pwm_b.ChangeDutyCycle(dutycycle)

  def ch_b_reverse(self, dutycycle):
    self.set_gpio(self.ch_b_input,[GPIO.HIGH, GPIO.LOW])
    self.pwm_b.ChangeDutyCycle(dutycycle)

  def ch_a_stop(self):
    self.set_gpio(self.ch_a_input,[GPIO.LOW, GPIO.LOW])
    self.pwm_a.ChangeDutyCycle(0)

  def ch_b_stop(self):
    self.set_gpio(self.ch_b_input,[GPIO.LOW, GPIO.LOW])
    self.pwm_b.ChangeDutyCycle(0)

  def set_gpio(self, pins, values):
    for index,pin in enumerate(pins):
      GPIO.output(pin, values[index])

  def setup_gpio(self, pins, values):
    for index,pin in enumerate(pins):
      GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
