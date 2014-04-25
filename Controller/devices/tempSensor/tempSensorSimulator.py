from devices.deviceBase import *
import random

class tempSensorSimulator(deviceBase):
	reading = None

	def __init__(self, deviceInfo, actionList, DB, logger):
		deviceBase.__init__(self, deviceInfo, actionList, DB, logger)

	def _processNewReading(self):
		self._DB.insertDeviceReading(self.iddevice, self.reading)
		for action in self._actionList:
			if(action.checkValue(self.reading)):
				self._DB.addCommand(action.idOutputDevice, action.iddeviceCommand, [action.value])

	def getReading(self):
		returnValue = None
		if(self.status):
			self.reading = random.uniform(23, 28)
			self._processNewReading()
			returnValue = self.reading
			self._logger.info( "deviceId: {0}, deviceName: {1}, reading: {2}".format(self.iddevice, self.deviceName, self.reading))

		else:
			self._logger.error( "{0}:{1}:Unable to take reading as sensor it turned off".format(self.iddevice, self.deviceName))

		return returnValue