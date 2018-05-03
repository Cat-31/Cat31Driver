import time, threading
from device import SteeringEngineDriver as sedriver, L298NDriver as l298n, HCSR04 as hcsr04, LED as led


class SmartCar(object):
    def __init__(self, config):
        self.init_green_led(config['green_led'])
        self.init_yellow_led(config['yellow_led'])
        self.init_front_steering_engine(config['front_steering_engine'])
        self.init_ud_steering_engine(config['ud_steering_engine'])
        self.init_l298n(config['l298n'])
        self.init_hcsr04(config['hcsr04'])

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

    def init_ud_steering_engine(self, config):
        self.ud_steering_engine = sedriver.SteeringEngine(config)

    def init_hcsr04(self, config):
        self.ud = hcsr04.HCSR04(config)
        self.distance_to_obstacle = -1
        self.ud_interval = config['interval']

    def camera_turn_to(self, angle):
        self.ud_steering_engine.move_to(180 - angle)  # 和前桥舵机相反

    def init_l298n(self, config):
        self.l298n = l298n.L298N(config)
        self.running = False

    def car_forward(self, dutycycle):
        if not self.running:
            self.running = True
            check_distance_thread = threading.Thread(target=self.check_distance, name='check distance thread')
            check_distance_thread.start()
            self.l298n.ch_a_start_up(dutycycle)
            self.l298n.ch_b_start_up(dutycycle)

    def car_back_off(self, dutycycle):
        self.l298n.ch_a_reverse(dutycycle)
        self.l298n.ch_b_reverse(dutycycle)

    def car_stop(self):
        self.l298n.ch_a_stop()
        self.l298n.ch_b_stop()
        self.running = False

    def set_distance_to_obstacle(self):
        self.ud_start = True
        while self.ud_start:
            self.distance_to_obstacle = self.ud.get_distance()
            if self.distance_to_obstacle < 0.2:
                self.set_yellow_led_on()
                self.set_green_led_off()
            else:
                self.set_yellow_led_off()
                self.set_green_led_on()

            time.sleep(self.ud_interval)

    def ud_stop(self):
        self.ud_start = False

    def ud_start(self):
        ud_thread = threading.Thread(target=self.set_distance_to_obstacle, name='ultrasonic distance measurement')
        ud_thread.start()

    def check_distance(self):
        while self.running:
            if self.distance_to_obstacle < 0.2:
                self.car_stop()
                self.running = False
            time.sleep(0.1)

    def exit(self):
        self.ud_stop()
