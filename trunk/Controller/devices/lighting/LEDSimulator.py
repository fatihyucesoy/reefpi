from devices.deviceBase import *

class LEDSimulator(deviceBase):

	def __init__(self, deviceInfo, actionList, DB):
		deviceBase.__init__(self, deviceInfo, actionList, DB)

	def setOutput(self, level):
		self._DB.setDeviceLevel(self.deviceName, level)
		self.level = level
		print "{0}: setting level to {1}".format(self.deviceName, self.level)
		return self.level
