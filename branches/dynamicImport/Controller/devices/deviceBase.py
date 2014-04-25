from DBInterface.SQLInterface import *


#This class will create and maintain a connection to the db
#as this is intended to run in its own thread,
#having its own connection sorts out thread crossing issues.  All communication
#should be done via the DB or in a thread safe way
class deviceBase:
	status = 0
	iddevice = 0
	deviceName= None
	iddeviceType = None
	deviceTypeName = None
	address = None
	level = None
	_DB = None
	_actionList = None
	_logger = None

	def __init__(self, deviceInfo, actionList, DB, logger):
		self.iddevice = deviceInfo['iddevice']
		self.deviceName = deviceInfo['deviceName']
		self.iddeviceType = deviceInfo['iddeviceType']
		self.address = deviceInfo['deviceAddress']
		self.status = deviceInfo['deviceStatus']
		self._actionList = actionList
		# TODO: reaffirm the state on start up.  This makes sure things stay in sync
		# over power cycles.
		self._DB = DB
		self._setState(self.status)
		self.level = deviceInfo['deviceLevel']
		self._logger = logger

	def init(self):
		self._setState(self.status)
		self.setOutput(self.level)

	def _setState(self, state):
		self._DB.setDeviceStatus(self.iddevice, state)
		self.status = state
		return self.status

	def turnOn(self):
		self._logger.info("Turning {0} On".format(self.deviceName,))
		return self._setState(1)

	def turnOff(self):
		slef._logger("Turning {0} Off".format(self.deviceName,))
		return self._setState(0)
