class sensorAction:
	idsensorAction = 0
	idsensor = None
	sensorName = None
	value = None
	relation = None
	type = None
	iddevice = None
	deviceName = None
	iddeviceCommand = None
	command = None


	def __init__(self, action):
		self.idsensorAction = action['idsensorAction']
		self.idsensor = action['idsensor']
		self.sensorName = action['sensorName']
		self.value = action['value']
		self.relation = action['sensorActionRelation']
		self.type = action['sensorActionType']
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
