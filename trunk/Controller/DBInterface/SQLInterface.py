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
					print 'Failed to run statement {0} due to error {1}'.format(statement, e)
					exit(0)
				statement = ''

	def configure(self):
		con = self._connect()
		with con:
			cur = con.cursor()
			self.execSqlFile(cur, "../DataBase/"+self._dataBase+".sql")

	def addBusType(self, name, desc):
		con = self._connect()
		with con:
			cur = con.cursor()
			test = cur.execute("""INSERT INTO busType (busTypeName, busTypeDescription)
									VALUES(%s, %s)""", (name, desc))
			con.commit()

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

	def addDeviceActionType(self, name, desc):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceActionType (deviceActionType, deviceActionTypeDescription)
							VALUES (%s, %s)""", (name, desc))
			con.commit()

	def addDeviceActionRelation(self, relation, symbol, desc):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceActionRelation
							(deviceActionRelation, deviceActionRelationSymbol, deviceActionRelationDescription)
							VALUES (%s, %s, %s)""", (relation, symbol, desc))
			con.commit()

	def addDeviceType(self, name, busType):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceType (deviceTypeName, idbusType)
							VALUES (%s, %s)""", (name, busType))
			con.commit()

	def addDeviceCommand(self, command, description):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceCommand (deviceCommand, deviceCommandDescription)
							VALUES (%s, %s)""", (command, description))
			con.commit()

	def addDevice(self, deviceName, type, address, defaultState, idController, level):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO device (deviceName, iddeviceType,
											   idcontroller, deviceAddress, deviceStatus, deviceLevel)
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

	def addDeviceAction(self, value, relation, type, iddevice, action, param):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceAction (deviceActionValue, iddeviceActionRelation,
													 iddeviceActionType, iddevice,
													 iddeviceCommand, deviceCommandParam)
							VALUES (%s, %s, %s, %s, %s, %s)""",\
							(value, relation, type, iddevice, action, param))
			con.commit()

	def insertDeviceReading(self, iddevice, reading):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""INSERT INTO deviceReading(iddevice, deviceReading) VALUES(%s, %s)""", (iddevice, reading))
			con.commit()


	def setDeviceStatus(self, deviceId, status):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""UPDATE device SET deviceStatus=%s
							WHERE iddevice=%s """
							,(status, deviceId))
			con.commit()

	def setDeviceLevel(self, deviceId, level):
		con = self._connect()
		with con:
			cur = con.cursor()
			cur.execute("""UPDATE device SET deviceLevel=%s
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


	def getAllDeviceReadings(self):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM deviceReading")
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

	def getAllScheduledEvents(self):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM scheduledEvent AS SE											\
							INNER JOIN scheduleType AS ST ON SE.idscheduleType = ST.idscheduleType 	\
							INNER join device AS D ON SE.iddevice = D.iddevice 						\
							INNER join deviceCommand AS DC on SE.iddeviceCommand = DC.iddeviceCommand")
    		return cur.fetchall()

	def getAllDeviceActions(self, iddevice):
		con = self._connect()
		with con:
			cur = con.cursor()
    		cur.execute("SELECT * FROM deviceAction AS DA \
				INNER JOIN device AS D ON DA.iddevice = D.iddevice \
				INNER JOIN deviceActionRelation AS DAR ON DA.iddeviceActionRelation = DAR.iddeviceActionRelation \
				INNER JOIN deviceCommand AS DC ON DA.iddeviceCommand = DC.iddeviceCommand \
				INNER JOIN deviceActionType AS DAT ON DA.iddeviceActionType = DAT.iddeviceActionType \
				where DA.iddevice = %s", (iddevice, ))
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




