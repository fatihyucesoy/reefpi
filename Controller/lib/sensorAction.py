class sensorAction:
	idSensorAction = 0
	idsensor = None
	value = None
	relation = None
	type = None
	iddevice = None
	action = None

	
	def __init__(self, action):
		self.idSensorAction = action[0]
		self.idsensor = action[1]
		self.value = action[2]
		self.relation = action[3]
		self.type = action[4]
		self.iddevice = action[5]
		self.action = action[6]
		#self._printParameters()
		
	def _printParameters(self):
		print """idSensorAction		={0},
				idsensor		={1}, 
				value	={2}, 
				relation		={3}, 
				type		={4},
				iddevice		={5}, 
				action		={6}""".format(self.idSensorAction, 
				self.idsensor, self.value, self.relation, \
				self.type, self.iddevice, self.action)
		
	
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
