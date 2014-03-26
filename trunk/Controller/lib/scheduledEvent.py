class scheduledEvent:
	Id = 0
	name = None
	type = None
	deviceId = None
	state = None
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
	
	def __init__(self, Id, name, type, deviceId=None, \
				state=None, value=None, startDate=None, 			\
				year=None, month=None, day=None, week=None, \
				day_of_week=None, hour=None, minute=None, second=None):
		#self._printParameters()
		self.Id = Id
		self.name = name
		self.type = type
		self.deviceId = deviceId
		self.state = state
		self.startDate = startDate
		self.value = value
		self.year = year
		self.month = month
		self.day = day
		self.week = week
		self.day_of_week = day_of_week
		self.hour = hour
		self.minute = minute
		self.second = second
		
	def _printParameters(self):
		print '''				id 		={0},
				name		={1},
				type		={2}, 
				deviceId	={3}, 
				state		={4}, 
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
				self.state, self.startDate, self.value, self.year, \
				self.month, self.day, self.week, self.day_of_week, \
				self.hour, self.minute, self.second)
		
	

