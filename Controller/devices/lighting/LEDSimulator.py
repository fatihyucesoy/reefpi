from devices.deviceBase import *

class LEDSimulator(deviceBase):

	def __init__(self, deviceInfo, actionList, DB, logger):
		deviceBase.__init__(self, deviceInfo, actionList, DB, logger)

	def setOutput(self, level):
		self._DB.setDeviceLevel(self.deviceName, level)
		self.level = level
		self._logger.info( "{0}: setting level to {1}".format(self.deviceName, self.level))
		return self.level
