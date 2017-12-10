import RPi.GPIO as GPIO
import signal
import atexit
import SmartCar as smartcar
import cv2
import numpy as np
import sys,time

GPIO.setmode(GPIO.BCM)
atexit.register(GPIO.cleanup)

config  = {'green_led':{'pin':3, 'on':True}, 
           'yellow_led':{'pin':2, 'on':True}, 
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


def calHist(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  
  lower_blue = np.array([110, 50, 50])
  upper_blue = np.array([130, 255, 255])
  
  mask = cv2.inRange(hsv, lower_blue, upper_blue)
  
  kernel = np.ones((3,3), np.uint8)
  erosion = cv2.erode(mask, kernel, iterations = 2)
  
  dilation = cv2.dilate(erosion, kernel, iterations = 1)
  res = cv2.bitwise_and(img, img, mask= dilation)
  originHist = cv2.calcHist([res], [0], mask, [256], [0, 256])
  return originHist, res

def polyHist(hist, color):
  h = np.zeros((256, 256, 3))
  bins = np.arange(256).reshape(256,1)
  cv2.normalize(hist, hist, 0, 255*0.9, cv2.NORM_MINMAX)
  hist = np.int32(np.around(hist))
  pts = np.column_stack((bins, hist))
  cv2.polylines(h, [pts], False, color) 
  return np.flipud(h)

def startCV():
  global car
  im = cv2.imread('img/flash.png')
  flashHist, falshRes = calHist(im)
  hight, wight = falshRes.shape[0:2]
  
  cap = cv2.VideoCapture(0)
  i = 100
  while True:
    h = polyHist(flashHist, (255, 255, 255))
    output = np.zeros((736, 1280, 3))
    output[-256:, wight:wight+256] = h
    output[-hight:, 0:wight] = falshRes

    _, frame = cap.read()
    
    currentHist, resImg = calHist(frame)

    if currentHist is not None:
      h = polyHist(currentHist,(0, 0, 255))
      output[-256:, 640:896] = h
      output[0:480,0:640] = frame
      
      comp = cv2.compareHist(flashHist, currentHist, cv2.HISTCMP_BHATTACHARYYA)
      if comp <= 0.5:
        car.flash_light_on(80)
        time.sleep(5)
        car.flash_light_off()

      font=cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(resImg,str('%0.5f' %comp),(10,30), font, 1,(0,0,255),2)#加减10是调整字符位置
      output[0:480,-640:] = resImg
      cv2.imwrite(('/tmp/cv/output%03d.jpg' % (i%100)), output)
      i += 1
    #ch = cv2.waitKey(1) & 0xFF
    #if ch == ord('q'):
    #  break
  #cv2.destroyAllWindows()

startCV()
