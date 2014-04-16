class deviceAction:
	iddeviceAction = 0
	iddevice = None
	deviceName = None
	value = None
	relation = None
	type = None
	iddevice = None
	deviceName = None
	iddeviceCommand = None
	command = None


	def __init__(self, action):
		print action
		self.iddeviceAction = action['iddeviceAction']
		self.iddevice = action['iddevice']
		self.deviceName = action['deviceName']
		self.value = action['deviceActionValue']
		self.relation = action['deviceActionRelation']
		self.type = action['deviceActionType']
		self.iddevice = action['iddevice']
		self.deviceName = action['deviceName']
		self.iddeviceCommand = action['iddeviceCommand']
		self.command= action['deviceCommand']
		#self._printParameters()

	def _printParameters(self):
		print """iddeviceAction		={0},
				iddevice		={1},
				idSsensosrName = {2},
				value	={3},
				relation		={4},
				type		={5},
				iddevice		={6},
				command		={7},
				deviecName = {8},
				iddeviceCommand= {9}""".format(self.iddeviceAction,  \
				self.iddevice, self.deviceName, self.value, self.relation, \
				self.type, self.iddevice, self.command, self.deviceName, self.iddeviceCommand)


	def checkValue(self, value):

		result = False
		if(self.relation == 'lt'):
			if(value < self.value):
				result = True
		elif(self.relation =='gt'):
			if(value > self.value):
				result = True
		elif(self.relation == 'eq'):
			if(value == self.value):
				result = True
		elif(self.relation == 'neq'):
			if(value != self.value):
				result = True

		return result
