

import random
import time
import datetime

from DBInterface.SQLInterface import *


#This class will create and maintain a connection to the db
#as this is intended to run in its own thread,
#having its own connection sorts out thread crossing issues.  All communication
#should be done via the DB or in a thread safe way
class tempSimulator:
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
		self.level = ['deviceLevel']

	def _processNewReading(self):
		# TODO: add error checking as if this fails things might be bad.
		self._DB.insertSensorReading(self.iddevice, self.reading)
		for action in self.actionList:
			if(action.checkValue(self.reading)):
				self._DB.addCommand(action.iddevice, action.iddeviceCommand, [action.value])

	def _setState(self, state):
		self._DB.setDeviceStatus(self.iddevice, state)
		self.status = state
		return self.status

	def turnOn(self):
		print "Turning {0} On".format(deviceName,)
		return self._setState(1)

	def turnOff(self):
		print "Turning {0} Off".format(deviceName,)
		return self._setState(0)

	def takeNewReading(self):
		if(self.status):
			print "deviceId: {0}, deviceName: {1}, reading: {2}".format(self.iddevice, self.deviceName, self.reading)
			self.reading = random.uniform(23, 28)
			self._processNewReading()
		else:
			print "{0}:{1}:Unable to take reading as sensor it turned off".format(self.iddevice, self.deviceName)
		return self.reading