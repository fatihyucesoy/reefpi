from DBInterface.SQLInterface import *

class heaterSimulator:
	_heaterState = 0
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
		print self._name +': Turning heater on'
		self._DB.setDeviceStatus(self._Id, 1)
		self._heaterState = 1
		return self._heaterState
		
	
	def turnDeviceOff(self):
		print self._name + ': Turning heater off'
		self._DB.setDeviceStatus(self._Id, 0)
		self._heaterState = 0
		return self._heaterState
		
	def getId(self):
		return self._Id
