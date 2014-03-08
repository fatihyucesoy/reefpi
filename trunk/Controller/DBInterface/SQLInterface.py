import MySQLdb as sql

class SQLInterface:

	def _connect(self):
		return sql.connect(host="localhost", # your host, usually localhost
                     user="root",
                      db="reefPi_RPi_schema")
	def config(self):
		import os
		os.system('mysql -u root < ../DataBase/reefPi_RPi_schema.sql')	
		
		
	def addSensor(self, sensorID, type, address, minTemp, maxTemp, device, period):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensors VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s)""", (sensorID, type, address, minTemp, maxTemp, device, period))
			con.commit()
			
	def addDevice(self, deviceID, type, address):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO devices VALUES(NULL, %s, %s, %s)""", (deviceID, type, address))
			con.commit()		
			
	def insertSensorReading(self, probeId, temp):
		con = self._connect()
		with con:
			cur = con.cursor() 
			cur.execute("""INSERT INTO sensorReadings VALUES(NULL, CURRENT_TIMESTAMP, %s, %s)""", (probeId, temp,))
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
			
			
	