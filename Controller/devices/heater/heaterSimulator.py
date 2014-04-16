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
	_actionList = None

	def __init__(self, deviceInfo, actionList, DB):
		self.Iddevice = deviceInfo['iddevice']
		self.deviceName = deviceInfo['deviceName']
		self.iddeviceType = deviceInfo['iddeviceType']
		self.address = deviceInfo['deviceAddress']
		self.status = deviceInfo['deviceStatus']
		self._actionList = actionList
		# TODO: reaffirm the state on start up.  This makes sure things stay in sync
		# over power cycles.
		self._DB = DB
		self._setState(self.status)

	def _setState(self, state):
		self._DB.setDeviceStatus(self.iddevice, state)
		self.status = state
		return self.status

	def turnOn(self):
		print self.deviceName +': Turning heater on'
		return self._setState(1)

	def turnOff(self):
		print self.deviceName + ': Turning heater off'
		return self._setState(0)

