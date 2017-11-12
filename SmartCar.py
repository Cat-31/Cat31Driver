import RPi.GPIO as GPIO
import time
import signal
import atexit
from bottle import route, run, static_file, response
from device import SteeringEngineDriver as sedriver, L298NDriver as l298n, HCSR04 as hcsr04, LED as led

class SmartCar(object):
  def __init__(self,config):
    self.init_green_led(config['green_led'])
    self.init_yellow_led(config['yellow_led'])
    self.init_front_steering_engine(config['front_steering_engine'])
    self.init_camera_steering_engine(config['camera_steering_engine'])
    self.init_l298n(config['l298n'])
    #self.init_hcsr04(config['hcsr04'])
  
  def init_green_led(self, config):
    self.green_led = led.LED(config)
  
  def init_yellow_led(self, config):
    self.yellow_led = led.LED(config)
  
  def set_green_led_on(self):
    self.green_led.on()
  
  def set_green_led_off(self):
    self.green_led.off()
  
  def set_yellow_led_on(self):
    self.yellow_led.on()

  def set_yellow_led_off(self):
    self.yellow_led.off()

  def init_front_steering_engine(self, config):
    self.front_steering_engine = sedriver.SteeringEngine(config)
  
  def direction_turn_to(self, angle):
    self.front_steering_engine.move_to(angle)
    
  def init_camera_steering_engine(self, config):
    self.camera_steering_engine = sedriver.SteeringEngine(config)
  
  def camera_turn_to(self, angle):
    self.camera_steering_engine.move_to(180-angle)  # 和前桥舵机相反
    
  def init_l298n(self, config):
    self.l298n = l298n.L298N(config)
    
  def flash_light_on(self, dutycycle):
    self.l298n.ch_b_start_up(50)
	
  def flash_light_off(self, dutycycle):
    self.l298n.ch_b_stop()

  def car_forward(self, dutycycle):
    self.l298n.ch_a_start_up(30)
	
  def car_back_off(self, dutycycle):
    self.l298n.ch_a_reverse(30)

  def car_stop(self):
    self.l298n.ch_a_stop()




