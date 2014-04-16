class scheduledEvent:
	idscheduledEvent = 0
	jobName = None
	idscheduleType = None
	scheduleTypeName = None
	iddevice = None
	deviceName = None
	iddeviceCommand = None
	deviceCommand = None
	value = None
	startDate = None
	year = None
	month = None
	day = None
	week = None
	day_of_week = None
	hour = None
	minute = None
	second = None

	def __init__(self, event):
		self.idscheduledEvent = event['idscheduledEvent']
		self.jobName = event['jobName']
		self.idscheduleType = event['idscheduleType']
		self.scheduleTypeName = event['scheduleTypeName']
		self.iddevice = event['iddevice']
		self.deviceName = event['deviceName']
		self.iddeviceCommand = event['iddeviceCommand']
		self.deviceCommand = event['deviceCommand']
		self.value = event['value']
		self.startDate = event['startDate']
		self.year = event['year']
		self.month = event['month']
		self.day = event['day']
		self.week = event['week']
		self.day_of_week = event['day_of_week']
		self.hour = event['hour']
		self.minute = event['minute']
		self.second = event['second']



