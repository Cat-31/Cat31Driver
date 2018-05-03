import RPi.GPIO as GPIO
import time
import signal
import atexit
import SmartCar as smartcar
from bottle import route, run, static_file, response

GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

config = {'green_led': {'pin': 27, 'on': True},
          'yellow_led': {'pin': 22, 'on': True},
          'front_steering_engine': {'pin': 20, 'angle': 90},
          'ud_steering_engine': {'pin': 21, 'angle': 90},
          'l298n': {
              'ch_a': {
                  'pins': [6, 13], 'pwm': {'pin': 16, 'frq': 90}
              },
              'ch_b': {
                  'pins': [19, 26], 'pwm': {'pin': 5, 'frq': 90}
              }
          },
          'hcsr04': {'pins': {'T': 23, 'R': 24}, 'interval': 0.1, 'voice_speed': 340}
          }

car = smartcar.SmartCar(config)
car.ud_start()
atexit.register(car.exit)

front_angle = config['front_steering_engine']['angle']
ud_angle = config['ud_steering_engine']['angle']


def forward():
    print('forward')
    global car
    car.car_forward(30)


def back():
    print('back')
    global car
    car.car_back_off(30)


def stop():
    print('stop')
    global car
    car.car_stop()


def turn_left():
    global car, front_angle
    front_angle = front_angle - 10
    print('turn_left: %d' % front_angle)
    car.direction_turn_to(front_angle)


def turn_right():
    global car, front_angle
    front_angle = front_angle + 10
    print('turn_right: %d' % front_angle)
    car.direction_turn_to(front_angle)


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


@route('/cat31/<filename>')
def send_static(filename):
    response.content_type = 'text/html; charset=UTF-8'
    return static_file(filename, root='./')


@route('/cat31/static/<filename>')
def send_js(filename):
    response.content_type = 'script/javascript; charset=UTF-8'
    return static_file(filename, root='./static/')


@route('/cat31/control/<action>')
def car_control(action):
    control(action)


def control(action):
    control = {
        'forward': lambda: forward(),
        'back': lambda: back(),
        'left': lambda: turn_left(),
        'right': lambda: turn_right(),
        'stop': lambda: stop(),
        'udleft': lambda: ud_turn_left(),
        'udright': lambda: ud_turn_right()
    }
    return control[action]()


run(host='0.0.0.0', port=80)
