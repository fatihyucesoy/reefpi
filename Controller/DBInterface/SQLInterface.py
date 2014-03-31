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
			createString = "mysql -u "+self._user+" -p"+self._passwd+" < ../DataBase/"+self._dataBase+".sql"
		else:
			createString = "mysql -u "+self._user+" < ../DataBase/"+self._dataBase+".sql"
		print createString
		os.system(createString)	
		
	
	def addControllerType(self, name, desc):
		con = self._connect()
		with con:
			cur = con.cursor() 
			test = cur.execute("""INSERT INTO controllerType (controllerTypeName, ControllerTypeDescription)
									VALUES(%s, %s)""", (name, desc))
			con.commit()
			
	def addController(self, name, desc, type):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO controller (controllerName, idcontrollerType, controllerDescription)
							VALUES(%s, %s, %s)""", (name, type, desc))
			con.commit()
			
	def addDeviceType(self, name, busType):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO deviceType (deviceTypeName, busType) 
							VALUES (%s, %s)""", (name, busType))
			con.commit()
	
	def addSensorType(self, type, busType):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensorType (sensorTypeName, busType)
							VALUES(%s, %s)""", (type, busType))
			con.commit()
		
	def addSensor(self, sensorID, type, address, units, period):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensor (sensorName, idsensorType, address, units, period)
							VALUES(%s, %s, %s, %s, %s)""", (sensorID, type, address, units, period))
			con.commit()
			
	def addDevice(self, deviceName, type, address, defaultState, idController, level):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO device (deviceName, iddeviceType, idcontroller, address, status, level) 
							VALUES(%s, %s, %s, %s, %s, %s)""", \
			(deviceName, type, idController, address, defaultState, level))
			con.commit()
			
			
	def addScheduledEvent(self, name, type, deviceId=None, command=None, value=None, startDate=None, \
							year=None, month=None, day=None, week=None, day_of_week=None, 				\
							hour=None, minute=None, second=None):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""insert into scheduledEvent values (default, %s, %s, %s, %s, %s, %s, %s, 
							%s, %s, %s, %s, %s, %s,%s)""",
							(name, type, deviceId, command, value, startDate,			\
							year, month, day, week, day_of_week, 					\
							hour, minute, second))
			con.commit()
				
	def addSensorAction(self, idSensor, value, relation, type, iddevice, action):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensorAction (idsensor, value, relation, type, iddevice, action) 
							VALUES (%s, %s, %s, %s, %s, %s)""",\
							(idSensor, value, relation, type, iddevice, action))
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
			cur.execute("""UPDATE device SET Status=%s
							WHERE iddevice=%s """
							,(status, deviceId))
			con.commit()
			
	def setDeviceLevel(self, deviceId, level):
		con = self._connect()
		with con:
			cur = con.cursor()    
			cur.execute("""UPDATE device SET level=%s
							WHERE iddevice=%s """
							,(level, deviceId))

			con.commit()
								
	def getAllDevices(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
			cur.execute("SELECT * FROM device")
			return cur.fetchall()
			
	def getAllSensors(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensor")
    		return cur.fetchall()

       				
	def getAllSensorReadings(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensorReadings")
    		return cur.fetchall()
    			
	def getNextCommand(self):
		command = None
		deviceId = None
		commandId = None
		param = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM commands LIMIT 1")
    		command = cur.fetchone()
    		if(command != None):
    			deviceId = command[1]
    			commandId = command[2]
    			param = command[3]
    			cur.execute("""DELETE FROM commands where IdCommands = %s""", (command[0],))
    			con.commit()
		
		return (deviceId, commandId, param)
		
	def getSensorType(self, sensorTypeId):	
		type = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("""SELECT sensorTypeName FROM sensorType where idsensorType = %s""", (sensorTypeId, ))
    		type = cur.fetchone()
    		
		return type[0]
	
	def getAllScheduledEvents(self):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("select * from scheduledEvent")
    		return cur.fetchall()
	
	def getAllSensorActions(self, idSensor):
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("select * from sensorAction WHERE idsensor = %s", (idSensor, ))
    		return cur.fetchall()
		
	
	def getDeviceType(self, deviceTypeId):	
		device = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("""SELECT deviceTypeName FROM deviceType where iddeviceType = %s""", (deviceTypeId, ))
    		device = cur.fetchone()    		
		return device[0]
		
			
	def addCommand(self, deviceId, command, args):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO commands (iddevice, command, parameterlist)VALUES(%s, %s, %s)""", (deviceId, command, args))
			con.commit() 
			
					
			
		
