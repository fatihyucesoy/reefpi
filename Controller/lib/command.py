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




