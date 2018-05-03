#! /usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO


class LED(object):
    def __init__(self, config):
        self.pin = config['pin']
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)

        if config['on']:
            GPIO.output(self.pin, GPIO.HIGH)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
