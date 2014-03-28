import MySQLdb as sql
import os

class SQLInterface:

	_host = "localhost"
	_user = "root"
	_passwd = ""
	_dataBase = "reefPi_RPi_schema"
	
	def _connect(self):
		return sql.connect(host=self._host,
							user=self._user,
							passwd=self._passwd,
							db=self._dataBase)
	
	def __init__(self, host, user, passwd, dataBase):
		
		self._host = host
		self._user = user
		self._passwd = passwd
		self._dataBase = dataBase
		
	def configure(self):
		createString=""
		
		if(self._passwd!=""):
			createString = "mysql -u "+self._user+" -p"+self._passwd+" < ../DataBase/reef"+self._dataBase+".sql"
		else:
			createString = "mysql -u "+self._user+" < ../DataBase/"+self._dataBase+".sql"
		print createString
		os.system(createString)	
		
	
	def addControllerType(self, type, desc):
		con = self._connect()
		with con:
			cur = con.cursor() 
			test = cur.execute("""INSERT INTO controllerType VALUES(DEFAULT, %s, %s)""", \
			(type, desc))
			con.commit()
			
	def addController(self, name, desc, type):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO controller VALUES(DEFAULT, %s, %s, %s)""", \
			(name, desc, type))
			con.commit()
			
	def addDeviceType(self, type, busType):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO deviceType VALUES(DEFAULT, %s, %s)""", \
			(type, busType))
			con.commit()
	
	def addSensorType(self, type, busType):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensorType VALUES(DEFAULT, %s, %s)""", \
			(type, busType))
			con.commit()
		
	def addSensor(self, sensorID, type, address, minTemp, maxTemp, device, period):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensors VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)""", \
			(sensorID, type, address, minTemp, maxTemp, device, period))
			con.commit()
			
	def addDevice(self, deviceID, type, address, defaultState, idController, level):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO devices VALUES(NULL, %s, %s, %s, %s, %s, %s)""", \
			(deviceID, type, address, defaultState, idController, level))
			con.commit()
			
			
	def addScheduledEvent(self, name, type, deviceId=None, state=None, value=None, startDate=None, \
							year=None, month=None, day=None, week=None, day_of_week=None, 				\
							hour=None, minute=None, second=None):
		con = self._connect()
		with con:
			cur = con.cursor() 
			#"""insert into scheduledEvent values (default, "test", "crone", 1, 1, 100,
			#				now(), null, null, null, null, null, null, null, 6)"""
			cur.execute("""insert into scheduledEvent values (default, %s, %s, %s, %s, %s, %s, %s, 
							%s, %s, %s, %s, %s, %s,%s)""",
							(name, type, deviceId, state, value, startDate,			\
							year, month, day, week, day_of_week, 					\
							hour, minute, second))
			con.commit()
				
			
	def insertSensorReading(self, probeId, temp):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensorReadings VALUES(NULL, CURRENT_TIMESTAMP, %s, %s)""", (probeId, temp,))
			con.commit()
	
	
	def setDeviceStatus(self, deviceId, status):
		con = self._connect()
		with con:
			cur = con.cursor()    
			cur.execute("""UPDATE Devices SET Status=%s
							WHERE idDevices=%s """
							,(status, deviceId))
			con.commit()
			
	def setDeviceLevel(self, deviceId, level):
		con = self._connect()
		with con:
			cur = con.cursor()    
			cur.execute("""UPDATE devices SET level=%s
							WHERE idDevices=%s """
							,(level, deviceId))

			con.commit()
								
	def getAllDevices(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
			cur.execute("SELECT * FROM devices")
			return cur.fetchall()
			
	def getAllSensors(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensors")
    		return cur.fetchall()

       				
	def getAllSensorReadings(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensorReadings")
    		return cur.fetchall()
    			
	def getNextCommand(self):
		command = None
		commandId = None
		param = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM commands LIMIT 1")
    		command = cur.fetchone()
    		if(command != None):
    			commandId = command[1]
    			param = command[2]
    			cur.execute("""DELETE FROM commands where IdCommands = %s""", (command[0],))
    			con.commit()
		
		return (commandId, param)
		
	def getSensorType(self, sensorTypeId):	
		type = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("""SELECT sensorName FROM sensorType where idsensorType = %s""", (sensorTypeId, ))
    		type = cur.fetchone()
    		
		return type[0]
	
	def getAllScheduledEvents(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("select * from scheduledEvent")
    		return cur.fetchall()
		
	
	def getDeviceType(self, deviceTypeId):	
		device = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("""SELECT deviceName FROM deviceType where iddeviceType = %s""", (deviceTypeId, ))
    		device = cur.fetchone()    		
		return device[0]
		
			
	def addCommand(self, commandId, deviceId):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO commands VALUES(NULL, %s, %s)""", (commandId, deviceId))
			con.commit() 
			
					
			
	
