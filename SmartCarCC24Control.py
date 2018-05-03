import RPi.GPIO as GPIO
import time
import signal
import atexit
import SmartCarCC24 as smartcar
from bottle import route, run, static_file, response

GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

config = {'ud_steering_engine': {'pin': 21, 'angle': 90},
          'tb6612fng': {
              'ch_a': {
                  'pins': [6, 13], 'pwm': {'pin': 16, 'frq': 90}
              },
              'ch_b': {
                  'pins': [19, 26], 'pwm': {'pin': 5, 'frq': 90}
              },
              'stby': 20
          },
          'hcsr04': {'pins': {'T': 23, 'R': 24}, 'interval': 0.1, 'voice_speed': 340}
          }

car = smartcar.SmartCarCC24(config)
# car.ud_start()
# atexit.register(car.exit)

ud_angle = config['ud_steering_engine']['angle']


def set_left_speed(dc):
    global car
    car.set_left_forward(dc) if dc >=0 else car.set_left_reverse(-dc)


def set_right_speed(dc):
    global car
    car.set_right_forward(dc) if dc >= 0 else car.set_right_reverse(-dc)


def stop():
    print('stop')
    global car
    car.car_stop()


def ud_turn_left():
    global car, ud_angle
    ud_angle = ud_angle - 10
    print('camera_turn_left: %d' % ud_angle)
    car.camera_turn_to(ud_angle)


def ud_turn_right():
    global car, ud_angle
    ud_angle = ud_angle + 10
    print('camera_turn_right: %d' % ud_angle)
    car.camera_turn_to(ud_angle)


@route('/cc24/<filename>')
def send_static(filename):
    response.content_type = 'text/html; charset=UTF-8'
    return static_file(filename, root='./')


@route('/cc24/static/<filename>')
def send_js(filename):
    response.content_type = 'script/javascript; charset=UTF-8'
    return static_file(filename, root='./static/')


@route('/cc24/control/<action>/<value>')
def car_control(action, value):
    control(action, int(value))


def control(action, value):
    return {
        'setleft': lambda: set_left_speed(value),
        'setright': lambda: set_right_speed(value),
        'stop': lambda: stop(),
        'udleft': lambda: ud_turn_left(),
        'udright': lambda: ud_turn_right()
    }[action]()


run(host='0.0.0.0', port=80)
