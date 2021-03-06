import RPi.GPIO as GPIO
import time
import signal
import atexit
import SmartCar as car
from bottle import route, run, static_file, response
from device import SteeringEngineDriver as sedriver, L298NDriver as l298n, HCSR04 as hcsr04, LED as led

GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)
config = {'green_led': {'pin': 3, 'on': True},
          'yellow_led': {'pin': 2, 'on': True},
          'front_steering_engine': {'pin': 20, 'angle': 90},
          'camera_steering_engine': {'pin': 21, 'angle': 90},
          'l298n': {
              'ch_a': {
                  'pins': [6, 13], 'pwm': {'pin': 16, 'frq': 50}
              },
              'ch_b': {
                  'pins': [19, 26], 'pwm': {'pin': 5, 'frq': 0.5}
              }
          },
          'hcsr04': {'pins': {'T': 23, 'R': 24}, 'interval': 0.01, 'voice_speed': 340}
          }

car = car.SmartCar(config)

time.sleep(2)
car.set_yellow_led_off()

time.sleep(2)
car.set_green_led_off()

time.sleep(2)
car.set_yellow_led_on()

time.sleep(2)
car.set_green_led_on()

time.sleep(2)
car.direction_turn_to(100)
time.sleep(2)
car.camera_turn_to(100)

car.flash_light_on(80)
time.sleep(2)
car.flash_light_off()
time.sleep(2)
car.car_forward(30)
time.sleep(2)
car.car_back_off(50)
time.sleep(2)
car.car_stop()
time.sleep(2)
car.ud_start()
time.sleep(1)
print('distance %2f' % car.distance_to_obstacle)
time.sleep(1)
print('distance %2f' % car.distance_to_obstacle)

time.sleep(100)
car.ud_stop()
