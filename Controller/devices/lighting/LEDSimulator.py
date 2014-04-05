import web
import time


from DBInterface.SQLiteInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *


class LEDSimulator:
	status = 0
	iddevice = 0
	deviceName= None
	iddeviceType = None
	deviceTypeName = None
	address = None
	level = None
	_DB = None
	
	def __init__(self, deviceInfo, host, user, passwd, dataBase):
		self.Iddevice = deviceInfo['iddevice']
		self.deviceName = deviceInfo['deviceName']
		self.iddeviceType = deviceInfo['iddeviceType']
		self.address = deviceInfo['address']
		self.status = deviceInfo['status']
		# TODO: reaffirm the state on start up.  This makes sure things stay in sync
		# over power cycles.
		self._DB = SQLInterface(host, user, passwd, dataBase)
	
	def _setState(state):
		self._DB.setDeviceStatus(self.iddevice, state)
		self.status = state
		return self.status
		
	def turnOn(self):
		print self.deviceName +': Turning LED on'
		return self._setStatus(1)
	
	def turnOff(self):
		print self.deviceName + ': Turning LED off'
		return self._setStatus(0)
	
	def setIntensity(self, level):
		print self.deviceName + ': setting LED intensity to ' + str(level)
		self._DB.setDeviceLevel(self.deviceName, level)
		self.level = level
		return self.level	
		
	def getId(self):
		return self._Id
