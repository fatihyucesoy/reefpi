from DBInterface.SQLInterface import *

class heaterSimulator:
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
		self.level = deviceInfo['level']
		# TODO: reaffirm the state on start up.  This makes sure things stay in sync
		# over power cycles.
		self._DB = SQLInterface(host, user, passwd, dataBase)
	
	def _setState(state):
		self._DB.setDeviceStatus(self.iddevice, state)
		self.status = state
		return self.status
		
	def turnOn(self):
		print self._name +': Turning heater on'
		return self._setStatus(1)
	
	def turnOff(self):
		print self._name + ': Turning heater off'
		return self._setStatus(0)
		
