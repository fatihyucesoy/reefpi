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
		self.relation = action['relation']
		self.type = action['type']
		self.iddevice = action['iddevice']
		self.deviceName = action['deviceName']
		self.iddeviceCommand = action['iddeviceCommand']
		self.command= action['deviceCommand']
		#self._printParameters()
		
	def _printParameters(self):
		print """idSensorAction		={0},
				idsensor		={1}, 
				idSsensosrName = {2},
				value	={3}, 
				relation		={4}, 
				type		={5},
				iddevice		={6}, 
				command		={7},
				deviecName = {8},
				iddeviceCommand= {9}""".format(self.idsensorAction,  \
				self.idsensor, self.sensorName, self.value, self.relation, \
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
