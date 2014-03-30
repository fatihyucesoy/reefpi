import random
from DBInterface.SQLInterface import *


#This class will create and maintain a connection to the db
#as this is intended to run in its own thread,
#having its own connection sorts out thread crossing issues.  All communication
#should be done via the DB or in a thread safe way
class tempSimulator:
	_probeId = 0
	_probeName = 'None'
	_type = 'None'
	_address = 'None'
	_units = 'celcius'
	_period = 1
	_actionList = []
	#_reading = 25.5
	#_minReading = 0
	#_maxReading = 100
	#_deviceId = None
	#_period = 0
	#_host = "localhost"
	#_user = "root"
	#_passwd = ""
	#_dataBase = "reefPi_RPi_schema"
	#_DB = None
	
	def __init__(self, probeId, probeName, type, address, units, period, host, user, passwd, dataBase):
		self._probeId = probeId
		self._probeName = probeName
		self._type = type
		self._units = units
		self._period = period
		self._DB = SQLInterface(host, user, passwd, dataBase)
		
	def _processNewReading(self):
		# TODO: add error checking as if this fails things might be bad.
		self._DB.insertSensorReading(self._probeId, self._reading)
		
		for action in self._actionList:
			if(self._reading < self._minReading):
			#DB.turnHeaterOn(_getCommandID(turnHeaterOn))
				self._DB.addCommand(1, self._deviceId)
			else:
				#DB.turnHeateroff(_getCommandID(turnHeaterOff))
		 		self._DB.addCommand(2, self._deviceId)	
	
	def setActionList(self, actionList):
		self._actionList = actionList
			
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