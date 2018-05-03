import time, threading
from device import SteeringEngineDriver as sedriver, TB6612FNG as tb, HCSR04 as hcsr04


class SmartCarCC24(object):
    def __init__(self, config):
        self.ud_steering_engine = sedriver.SteeringEngine(config['ud_steering_engine'])
        self.ud = hcsr04.HCSR04(config['hcsr04'])
        self.distance_to_obstacle = -1
        self.ud_interval = config['hcsr04']['interval']
        self.tb6612fng = tb.TB6612FNG(config['tb6612fng'])
        self.running = False

    def set_left_forward(self, dutycycle):
        self.tb6612fng.ch_a_start_up(dutycycle)

    def set_left_reverse(self, dutycycle):
        self.tb6612fng.ch_a_reverse(dutycycle)

    def set_right_forward(self, dutycycle):
        self.tb6612fng.ch_b_start_up(dutycycle)

    def set_right_reverse(self, dutycycle):
        self.tb6612fng.ch_b_reverse(dutycycle)

    def car_stop(self):
        self.tb6612fng.ch_a_stop()
        self.tb6612fng.ch_b_stop()
