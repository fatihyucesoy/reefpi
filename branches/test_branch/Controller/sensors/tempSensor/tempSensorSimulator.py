import random

class tempSimulator:
	_probeID = 'NONE'
	_temp = 25.5
	_minTemp = 0
	_maxTemp = 100
	_heater = None
	
	def __init__(self, probeId, minTemp, maxTemp, heater):
		self._probeID = probeId
		self._minTemp = minTemp
		self._maxTemp = maxTemp
		self._heater = heater
		
	def getProbeID(self):
		return self._probeID
		
	def getTemp(self):
		self._temp = random.uniform(25,26)
		return self._temp;
	
	def getMinTemp(self):
		return self._minTemp
	
	def getMaxTemp(self):
		return self._maxTemp
	
	def getHeater(self):
		return self._heater