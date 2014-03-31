class scheduledEvent:
	Id = 0
	name = None
	type = None
	deviceId = None
	command = None
	startDate = None
	value = None
	year = None
	month = None
	day = None
	week = None
	day_of_week = None
	hour = None
	minute = None
	second = None
	
	def __init__(self, event):
		self.Id = event[0]
		self.name = event[1]
		self.type = event[2]
		self.deviceId = event[3]
		self.command = event[4]
		self.value = event[5]
		self.startDate = event[6]
		self.year = event[7]
		self.month = event[8]
		self.day = event[9]
		self.week = event[10]
		self.day_of_week = event[11]
		self.hour = event[12]
		self.minute = event[13]
		self.second = event[14]
		#self._printParameters()
		
	def _printParameters(self):
		print '''				id 		={0},
				name		={1},
				type		={2}, 
				deviceId	={3}, 
				command		={4}, 
				startDate	={5}, 
				value		={6}, 
				year		={7},
				month		={8},
				day		={9}, 
				week		={10},
				day_of_week	={11}, 
				hour		={12},
				min		={13}, 
				sec		={14}'''\
				.format(self.Id, self.name, self.type, self.deviceId, \
				self.command, self.startDate, self.value, self.year, \
				self.month, self.day, self.week, self.day_of_week, \
				self.hour, self.minute, self.second)
		
	

