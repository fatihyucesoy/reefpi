class deviceAction:
	iddeviceAction = 0
	iddevice = None
	idOutputDevice = None
	deviceName = None
	value = None
	relation = None
	type = None
	iddevice = None
	deviceName = None
	iddeviceCommand = None
	command = None


	def __init__(self, action):
		self.iddeviceAction = action['iddeviceAction']
		self.iddevice = action['idTargetDevice']
		self.idOutputDevice = action['idOutputDevice']
		self.deviceName = action['deviceName']
		self.value = action['deviceActionValue']
		self.relation = action['deviceActionRelation']
		self.type = action['deviceActionType']
		self.iddevice = action['iddevice']
		self.deviceName = action['deviceName']
		self.iddeviceCommand = action['iddeviceCommand']
		self.command= action['deviceCommand']


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
