class deviceCommand:
	Idcommand = 0
	iddevice = None
	deviceName = None

	iddeviceCommand = None
	deviceCommand = None
	args = []


	def __init__(self, command):
		self.Idcommand = command['idcommand']
		self.iddevice = command['iddevice']
		self.deviceName = command['deviceName']
		self.iddeviceCommand = command['iddeviceCommand']
		self.deviceCommand = command['deviceCommand']
		self.args = command['commandParam']
		#self._printParameters()

	def _printParameters(self):
		print '''				idcommand 		={0},
				iddevice		={1},
				device		={2},
				iddeviceCommand		={3},
				deviceCommand = {4}
				args	={5}'''\
				.format(self.Idcommand, \
				self.iddevice, \
				self.deviceName, \
				self.iddeviceCommand, \
				self.deviceCommand, \
				self.args)



