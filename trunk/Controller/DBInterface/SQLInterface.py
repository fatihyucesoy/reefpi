from __future__ import with_statement
import MySQLdb as sql
import MySQLdb.cursors
import os
import re

class SQLInterface:

	_host = "localhost"
	_user = "root"
	_passwd = ""
	_dataBase = "reefPi_RPi_schema"

	def _connect(self):
		return sql.connect(host=self._host,
							user=self._user,
							passwd=self._passwd,
							db=self._dataBase,
							cursorclass=MySQLdb.cursors.DictCursor)

	def __init__(self, host, user, passwd, dataBase):

		self._host = host
		self._user = user
		self._passwd = passwd
		self._dataBase = dataBase

	def execSqlFile(self, cursor, sql_file):
		print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
		statement =''
		for line in open(sql_file):
			if re.match(r'--', line):  # ignore sql comment lines
				continue
			if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
				statement = statement + line
			else:  # when you get a line ending in ';' then exec statement and reset for next statemen
				statement = statement + line
				try:
					if(not statement.isspace()):
						cursor.execute(statement)
				except Exception as e:
					exit(0)
				statement = ''

	def configure(self):
		con = self._connect()
		with con:
			cur = con.cursor()
			self.execSqlFile(cur, "../DataBase/"+self._dataBase+".sql")


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

	def addSensorActionType(self, name, desc):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO sensorActionType (sensorActionType, sensorActionTypeDescription)
							VALUES (%s, %s)""", (name, desc))
			con.commit()

	def addSensorActionRelation(self, relation, symbol, desc):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO sensorActionRelation
							(sensorActionRelation, sensorActionRelationSymbol, sensorActionRelationDescription)
							VALUES (%s, %s, %s)""", (relation, symbol, desc))
			con.commit()

	def addDeviceType(self, name, busType):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceType (deviceTypeName, busType)
							VALUES (%s, %s)""", (name, busType))
			con.commit()

	def addDeviceCommand(self, command, description):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceCommand (deviceCommand, deviceCommandDescription)
							VALUES (%s, %s)""", (command, description))
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

	def addScheduleType(self, type, description):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO scheduleType (scheduleTypeName, scheduleTypeDescription)
							VALUES (%s, %s)""", (type, description))
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
			cur.execute("""INSERT INTO sensorAction (idsensor, value, idsensorActionRelation, idsensorActionType, iddevice, iddeviceCommand)
							VALUES (%s, %s, %s, %s, %s, %s)""",\
							(idSensor, value, relation, type, iddevice, action))
			con.commit()

	def insertSensorReading(self, idsensor, reading):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO sensorReadings (idsensor, reading) VALUES(%s, %s)""", (idsensor, reading))
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
			cur.execute("SELECT * FROM device AS D INNER JOIN deviceType AS DT ON D.iddeviceType = DT.iddeviceType")
			return cur.fetchall()

	def getDevice(self, iddevice):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM device AS D \
						INNER JOIN deviceType AS DT ON D.iddeviceType = DT.iddeviceType \
						WHERE D.iddevice = %s", (iddevice,))
			return cur.fetchone()

	def getAllSensors(self):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM sensor AS S INNER JOIN sensorType AS ST ON S.idsensorType = ST.idsensorType")
    		return cur.fetchall()


	def getAllSensorReadings(self):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM sensorReadings")
    		return cur.fetchall()

	def getNextCommand(self):
		command = None
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM command AS C				\
							INNER JOIN device AS D ON C.iddevice = D.iddevice \
							INNER JOIN deviceCommand AS DC ON C.iddeviceCommand = DC.iddeviceCommand\
							LIMIT 1")
    		command = cur.fetchone()
    		if(command != None):
    			cur.execute("""DELETE FROM command where Idcommand = %s""", (command['idcommand'],))
    			con.commit()

		return command

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
    		cur.execute("SELECT * FROM scheduledEvent AS SE											\
							INNER JOIN scheduleType AS ST ON SE.idscheduleType = ST.idscheduleType 	\
							INNER join device AS D ON SE.iddevice = D.iddevice 						\
							INNER join deviceCommand AS DC on SE.iddeviceCommand = DC.iddeviceCommand")
    		return cur.fetchall()

	def getAllSensorActions(self, idSensor):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM sensorAction AS SA INNER JOIN device AS D ON SA.iddevice = D.iddevice 	\
							INNER join deviceCommand AS DC ON SA.iddeviceCommand = DC.iddeviceCommand 			\
							INNER JOIN sensor AS S ON SA.idsensor = S.idsensor									\
							INNER JOIN sensorActionType AS SAT ON SA.idsensorActionType = SAT.idsensorActionType \
							INNER JOIN sensorActionRelation AS SAR on SA.idsensorActionRelation = SAR.idsensorActionRelation \
							WHERE SA.iddevice = %s", (idSensor, ))
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
			cur.execute("""INSERT INTO command (iddevice, iddeviceCommand, parameterlist)VALUES(%s, %s, %s)""", (deviceId, command, args))
			con.commit()




