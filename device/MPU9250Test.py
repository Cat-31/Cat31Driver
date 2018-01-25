#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MPU9250 as mpu9250
import time

mpu = mpu9250.MPU9250()
print('Device connected:', mpu.searchDevice())

while True:
	if mpu.checkDataReady :
		print('readGyro', mpu.readGyro())
		print('readAccel', mpu.readAccel())
		print('readMagnet', mpu.readMagnet())
		print('readTemperature', mpu.readTemperature())
		print('')
		
	time.sleep(1)
