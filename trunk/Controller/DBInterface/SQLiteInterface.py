import sqlite3 as sql

class SQLiteInterface:	
	def createDateBase(self):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor()
			cur.execute("DROP TABLE IF EXISTS sensorReading")
			cur.execute("DROP TABLE IF EXISTS sensors")
			cur.execute("DROP TABLE IF EXISTS commands")
			cur.execute("DROP TABLE IF EXISTS devices")
			#TODO: the probeID should be FK to the sensor table
			cur.execute("CREATE TABLE sensorReading(Id INTEGER PRIMARY KEY NOT NULL, timeStamp DATETIME , probeID VARCHAR(1024), reading NUMERIC)")
			cur.execute("CREATE TABLE sensors(Id INTEGER PRIMARY KEY NOT NULL, SensorID  VARCHAR(1024), Type VARCHAR(255), address VARCHAR(255), lowerlimit FLOAT, upperlimit FLOAT, device VARCHAR(255))")
			cur.execute("CREATE TABLE commands(Id INTEGER PRIMARY KEY NOT NULL, commandID INT, parameterList VARCHAR(255))")
			cur.execute("CREATE TABLE devices(Id INTEGER PRIMARY KEY NOT NULL, deviceID  VARCHAR(1024), Type VARCHAR(255), address VARCHAR(255))")
	
	def addSensor(self, sensorID, type, address, minTemp, maxTemp, device):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO sensors VALUES(NULL, ?, ?, ?, ?, ?, ?)", (sensorID, type, address, minTemp, maxTemp, device))
			con.commit()
			
	def addDevice(self, deviceID, type, address):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO devices VALUES(NULL, ?, ?, ?)", (deviceID, type, address))
			con.commit()		
			
	def insertSensorReading(self, probeId, temp):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO sensorReading VALUES(NULL, CURRENT_TIMESTAMP, ?, ?)", (probeId, temp,))
			con.commit()
			
	def getAllDevices(self):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM devices")
    		return cur.fetchall()
    		
	def getAllSensors(self):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensors")
    		return cur.fetchall()

       				
	def getAllSensorReadings(self):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM sensorReadings")
    		return cur.fetchall()
    		
	def turnHeaterOn(self, commandId):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO commands VALUES(NULL, ?, 1)", (commandId,))
			con.commit() 
			
	def turnHeateroff(self, commandId):
		con = sql.connect('test.db')
		with con:
			cur = con.cursor() 
			cur.execute("INSERT INTO commands VALUES(NULL, ?, 0)", (commandId,))
			con.commit() 
			
	def getNextCommand(self):
		command = None
		commandId = None
		con = sql.connect('test.db')
		with con:
			cur = con.cursor()    
    		cur.execute("SELECT * FROM commands ORDER BY ROWID ASC LIMIT 1")
    		command = cur.fetchone()
    		if(command != None):
    			commandId = command[1]
    			cur.execute("DELETE FROM commands where Id = ?", (command[0],))
    			con.commit()
		
		return commandId
			
			
	