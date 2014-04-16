import random
import time
import datetime

from DBInterface.SQLInterface import *
from multiprocessing import Process


#This class will create and maintain a connection to the db
#as this is intended to run in its own thread,
#having its own connection sorts out thread crossing issues.  All communication
#should be done via the DB or in a thread safe way
class deviceBase:
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
		self.setOutput(self.level)

	def __init__(self, deviceInfo, actionList, database):
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
		self.setOutput(self.level)

	def _processNewReading(self):
		# TODO: add error checking as if this fails things might be bad.
		self._DB.insertSensorReading(self.idsensor, self.reading)
		for action in self.actionList:
			if(action.checkValue(self.reading)):
				self._DB.addCommand(action.iddevice, action.iddeviceCommand, [action.value])

	def stop (self):
		self._active = False;

	def setActionList(self, actionList):
		self._actionList = actionList

	def getProbeId(self):
		return self._probeId

	def takeNewReading(self):
		print "sensorId: {0}, sensorName: {1}, reading: {2}".format(self.idsensor, self.sensorName, self.reading)
		self.reading = random.uniform(23, 28)
		self._processNewReading()
		return self.reading