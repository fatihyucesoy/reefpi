import web
import time


from DBInterface.SQLiteInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *


class heaterSimulator:
	_heaterState = 0
	_Id = 0
	_name = None
	_type = None
	_address = None
	
	def __init__(self, Id, name, type, address):
		self._Id = Id
		self._name = name
		self._type = type
		self._address = address
	
	def turnDeviceOn(self):
		print self._name +': Turning heater on'
		self._heaterState = 1
		return self._heaterState
		
	
	def turnDeviceOff(self):
		print self._name + ': Turning heater off'
		self._heaterState = 0
		return self._heaterState
		
	def getId(self):
		return self._Id
