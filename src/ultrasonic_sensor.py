import RPi.GPIO as gpio
import time
from threading import Thread



class UltrasonicSensor:
    timeout = 0.05
	
    def __init__(self, trigger_pin, echo_pin, min, max):
        self.echo = echo_pin
		self.trigger = trigger_pin
        self.distance = 0
		self.min_dist = min
		self.max_dist = max
		gpio.setmode(gpio.BCM)
		gpio.setup(self.trigger, gpio.OUT)
		gpio.setup(self.echo, gpio.IN)
		
    def check_echo_started(self):
        return gpio.input(self.echo)
		
    def check_echo_ended(self):
        return not gpio.input(self.echo)
		
	def find_distance(self):
		time_check(self.check_echo_started, UltrasonicSensor.timeout)
		self.distance = micros_to_cm( time_check(
			self.check_echo_ended, UltrasonicSensor.timeout) * 1000000.0 )
		if self.distance < self.min_dist:
			self.distance = self.min_dist
		elif self.distance > self.max_dist:
			self.distance = self.max_dist
		
	def get_distance_thread(self):
		return Thread(target=find_distance, args=(self))
		
	def blip_freq(self):
		pass



def micros_to_cm(micros):
    return micros / 58.82

def micros_wait(t):
    tEnd = time.time() + t/1000000.0
    while time.time() < tEnd: pass

def time_check( return_checker, max_time ):
    tStart = time.time()
    tTimeout = tStart + max_time
    complete = return_checker()
    while not complete:
        complete = return_checker()
        if time.time() >= tTimeout: return 0.0
    return time.time() - tStart
    
