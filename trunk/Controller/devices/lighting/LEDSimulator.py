import web
import time


from DBInterface.SQLiteInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *


class LEDSimulator:
	_LEDState = 0
	level = 0
	_Id = 0
	_name = None
	_type = None
	_address = None
	_host = "localhost"
	_user = "root"
	_passwd = ""
	_dataBase = "reefPi_RPi_schema"
	_DB = None
	
	def __init__(self, Id, name, type, address, \
				host, user, passwd, dataBase):
		self._Id = Id
		self._name = name
		self._type = type
		self._address = address
		self._host = host
		self._user = user
		self._passwd = passwd
		self._dataBase = dataBase
		self._DB = SQLInterface(self._host, self._user, self._passwd, self._dataBase)
	
	def turnDeviceOn(self):
		print self._name +': Turning LED on'
		self._DB.setDeviceStatus(self._Id, 1)
		self._LEDState = 1
		return self._LEDState
		
	def turnDeviceOff(self):
		print self._name + ': Turning LED off'
		self._DB.setDeviceStatus(self._Id, 0)
		self._LEDState = 0
		return self._LEDState
	
	def setIntensity(self, level):
		print self._name + ': setting LED intensity to ' + str(level)
		self._DB.setDeviceLevel(self._Id, level)
		self.level = level
		return self.level	
		
	def getId(self):
		return self._Id
