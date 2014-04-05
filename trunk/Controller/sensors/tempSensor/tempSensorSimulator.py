import random
import time
import datetime

from DBInterface.SQLInterface import *
from multiprocessing import Process


#This class will create and maintain a connection to the db
#as this is intended to run in its own thread,
#having its own connection sorts out thread crossing issues.  All communication
#should be done via the DB or in a thread safe way
class tempSimulator:
	idsensor = 0
	sensorName = None
	idsensorType = None
	sensorTypeName = None
	busType = None
	address = 'None'
	units = 'celcius'
	period = 1
	actionList = []
	_active = False
	_DB = None
	reading = None
	
	def __init__(self, probeInfo, actionList, host, user, passwd, dataBase):
		print probeInfo 
		self.idsensor = probeInfo['idsensor']
		self.sensorName = probeInfo['sensorName']
		self.idsensorType = probeInfo['idsensorType']
		self.sensorTypeName = probeInfo['sensorTypeName']
		self.busType = probeInfo['busType']
		self.address = probeInfo['address']
		self.units = probeInfo['units']
		self.period = probeInfo['period']
		self.actionList = actionList
		self._DB = SQLInterface(host, user, passwd, dataBase)
		
	def _processNewReading(self):
		# TODO: add error checking as if this fails things might be bad.
		self._DB.insertSensorReading(self.idsensor, self.reading)
		for action in self.actionList:
			if(action.checkValue(self.reading)):
				self._DB.addCommand(action.iddevice, action.iddeviceCommand, [action.value])
	
	def _run(self):
		while(self._active):
			self.takeNewReading()
			print 'Sensor:' + str(self.sensorName) + ' current temp is:' + str(self.reading)	 	
			time.sleep(self.period)
		
	def run(self):
		self._active = True;
		process = Process(target=self._run, args=())
		process.start()
		return Process
	
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