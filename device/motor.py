import RPi.GPIO as GPIO
import time
import signal
import atexit
from bottle import route, run, static_file, response

dutyCycleWheel= 7
dutyCycleCamera = 7
pDirection = None
pCamera = None
pMotor = None
going = False
dutyCycleMotor = 30

atexit.register(GPIO.cleanup) 

def up():
        GPIO.output(6,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)

def down():
	GPIO.output(6,GPIO.HIGH)
	GPIO.output(13,GPIO.LOW)

def left():
	global dutyCycleWheel
	print(dutyCycleWheel)
	dutyCycleWheel = dutyCycleWheel - 0.5
	setSteeringEngine(pDirection, dutyCycleWheel)

def right():
	global dutyCycleWheel
	print(dutyCycleWheel)
	dutyCycleWheel = dutyCycleWheel + 0.5
	setSteeringEngine(pDirection, dutyCycleWheel)

def stop():
	global going
	going = False
	GPIO.output(6,GPIO.LOW)
	GPIO.output(13,GPIO.LOW)
	GPIO.output(19,GPIO.LOW)
	GPIO.output(26,GPIO.LOW)
	
def cameraRight():
	global dutyCycleCamera
	dutyCycleCamera = dutyCycleCamera - 0.2
	setSteeringEngine(pCamera, dutyCycleCamera)
	
def cameraLeft():
	global dutyCycleCamera
	dutyCycleCamera = dutyCycleCamera + 0.2
	setSteeringEngine(pCamera, dutyCycleCamera)

def setSteeringEngine(p, dutyCycle):
	for i in range(0,5,1):
		p.ChangeDutyCycle(dutyCycle) 
		time.sleep(0.02)					  
		p.ChangeDutyCycle(0)				  
	
def initSteeringEngine(pin, dutyCycle):
	GPIO.setup(pin, GPIO.OUT, initial=False)
	p = GPIO.PWM(pin,50) 
	p.start(0)
	setSteeringEngine(p,dutyCycle)
	return p

def initMotorPWM():
	GPIO.setup(16, GPIO.OUT, initial=False)
	global pMotor
	pMotor = GPIO.PWM(16,100)
	global dutyCycleMotor
	pMotor.start(dutyCycleMotor)
		
def initGPIO():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
   
	GPIO.setup(6, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(19, GPIO.OUT)
	GPIO.setup(26, GPIO.OUT)

	#disc
	GPIO.setup(23,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(24,GPIO.IN)

	#motor pmw
	#GPIO.setup(16,GPIO.OUT,initial=GPIO.HIGH)
	initMotorPWM()

	stop()
	global pDirection;
	global pCamera;
	
	pDirection = initSteeringEngine(20, dutyCycleWheel)
	pCamera = initSteeringEngine(21, dutyCycleCamera)
	
	print("init finisehd")



