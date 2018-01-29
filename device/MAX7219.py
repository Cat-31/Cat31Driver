#!/usr/bin/env python
# encoding: utf-8

import spidev

class MAX7219(object):
	def __init__(self):
		self.spi = spidev.SpiDev()
		self.spi.open(0, 0)
		set([0x0C, 0x01]) #关闭shutdown模式
		set([0x0B, 0x07]) #设置扫描范围为0-7

	def set(self, conf):
		self.spi.xfer2(conf)

	def show(self, arr):
		for i in range(len(arr)):
		    self.spi.xfer2([i+1, arr[i]])

