import random
from DBInterface.SQLInterface import *

class tempSimulator:
	_probeId = 0
	_probeName = 'None'
	_reading = 25.5
	_minReading = 0
	_maxReading = 100
	_deviceId = None
	_period = 0
	
	def __init__(self, probeId, probeName, minReading, maxReading, deviceId, period):
		self._probeId = probeId
		self._probeName = probeName
		self._minReading = minReading
		self._maxReading = maxReading
		self._deviceId = deviceId
		self._period = period
		
	def _processNewReading(self):
		DB     = SQLInterface()
		
		DB.insertSensorReading(self._probeId, self._reading)
		if(self._reading < self._minReading):
			#DB.turnHeaterOn(_getCommandID(turnHeaterOn))
			DB.turnDeviceOn(1, self._deviceId)
		else:
			#DB.turnHeateroff(_getCommandID(turnHeaterOff))
		 	DB.turnDeviceOff(2, self._deviceId)	
		
	def getProbeId(self):
		return self._probeId
		
	def takeNewReading(self):
		self._reading = random.uniform(25,26)
		self._processNewReading()
		return self._reading
		
	def getReading(self):
		return self._reading
		
	def getMinTemp(self):
		return self._minReading
	
	def getMaxTemp(self):
		return self._maxReading
	
	def getdeviceId(self):
		return self._deviceID
	
	def getPeriod(self):
		return self._period