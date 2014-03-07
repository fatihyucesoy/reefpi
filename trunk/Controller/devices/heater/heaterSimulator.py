import web
import time


from Database.SQLiteInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *


class heaterSimulator:
	heaterState = 0
	
	def turnHeaterOn(self):
		print 'turning heater on'
		self.heaterState = 1
		return self.heaterState
	
	def turnHeaterOff(self):
		print 'turning heater off'
		self.heaterState = 0
		return self.heaterState
