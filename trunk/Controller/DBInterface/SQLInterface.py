import MySQLdb as sql

class SQLInterface:

	def _connect(self):
		return sql.connect(host="localhost", # your host, usually localhost
                     user="root",
                      db="reefPi_RPi_schema")
	def config(self):
		import os
		os.system('mysql -u root < ../DataBase/reefPi_RPi_schema.sql')	
		
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
			
	def addDevice(self, deviceID, type, address, defaultState):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO devices VALUES(NULL, %s, %s, %s, %s)""", (deviceID, type, address, defaultState))
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
    		print type
    		
		return type[0]
	
	def getDeviceType(self, deviceTypeId):	
		device = None
		con = self._connect()
		with con:
			cur = con.cursor()    
    		cur.execute("""SELECT deviceName FROM deviceType where iddeviceType = %s""", (deviceTypeId, ))
    		device = cur.fetchone()
    		print device
    		
		return device[0]
		
			
	def turnDeviceOn(self, commandId, deviceId):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO commands VALUES(NULL, %s, %s)""", (commandId, deviceId))
			con.commit() 
			
	def turnDeviceOff(self, commandId, deviceId):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO commands VALUES(NULL, %s, %s)""", (commandId, deviceId))
			con.commit() 		
			
	