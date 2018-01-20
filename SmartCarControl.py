import RPi.GPIO as GPIO
import time
import signal
import atexit
import SmartCar as smartcar
from bottle import route, run, static_file, response

GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

config  = {'green_led':{'pin':27, 'on':True}, 
           'yellow_led':{'pin':22, 'on':True}, 
           'front_steering_engine':{'pin':20,'angle':90},
           'camera_steering_engine':{'pin':21,'angle':90},
           'l298n':{
                     'ch_a': {
                       'pins':[6,13],'pwm':{'pin':16,'frq':50}
                     },
                    'ch_b':{
                      'pins':[19,26],'pwm':{'pin':5,'frq':0.5}
                     }
                   },
            'hcsr04':{'pins':{'T':23,'R':24}, 'interval':0.1, 'voice_speed':340}
          }
           
car = smartcar.SmartCar(config)
car.ud_start()
atexit.register(car.exit)

front_angle = config['front_steering_engine']['angle']
camera_angle = config['camera_steering_engine']['angle']

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

def flashon():
  print('flashon')
  global car
  car.flash_light_on(50)
  
def flashoff():
  print('flashoff')
  global car
  car.flash_light_off()
  
def turn_left():
  global car,front_angle
  front_angle = front_angle - 10
  print('turn_left: %d' % front_angle)
  car.direction_turn_to(front_angle)
  
def turn_right():
  global car,front_angle
  front_angle = front_angle + 10
  print('turn_right: %d' % front_angle)
  car.direction_turn_to(front_angle)
  
def camera_turn_left():
  global car,camera_angle
  camera_angle = camera_angle - 10
  print('camera_turn_left: %d' % camera_angle)
  car.camera_turn_to(camera_angle)
  
def camera_turn_right():
  global car,camera_angle
  camera_angle = camera_angle + 10
  print('camera_turn_right: %d' % camera_angle)
  car.camera_turn_to(camera_angle)
  
@route('/cat31/<filename>')
def send_static(filename):
    response.content_type = 'text/html; charset=UTF-8'
    return static_file(filename, root='./')

@route('/cat31/control/<action>')
def car_control(action):
    control(action)

def control(action): 
    control = { 
               'forward'         :lambda:forward(), 
               'back'            :lambda:back(), 
               'left'            :lambda:turn_left(), 
               'right'           :lambda:turn_right(), 
               'stop'            :lambda:stop(),
               'cameraturnleft'  :lambda:camera_turn_left(),
               'cameraturnright' :lambda:camera_turn_right(),    
               'flashon'         :lambda:flashon(),  
               'flashoff'        :lambda:flashoff()		   
              } 
    return control[action]() 

run(host='0.0.0.0', port=80)
