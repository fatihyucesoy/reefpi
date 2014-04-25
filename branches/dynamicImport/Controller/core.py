import web
import time
import datetime
import inspect
import os
import imp
import importlib
from DBInterface.SQLInterface import *
from devices import *
from scheduler.reefPI_Scheduler import *
from lib.LEDIntensityCalculator import *
from lib.scheduledEvent import *
from lib.deviceAction import *
from lib.command import *
import logging
import logging.handlers



latitude = -19.770621   # + to N  Defualt - (-19.770621) Heart Reef, Great Barrier Reef, QLD, Australia
longitude = 149.238532  # + to E  Defualt - (149.238532)
TimeZone = 10			 # + to E  Defulat - (10)

host = "localhost"
user = "root"
passwd = ""
dataBase = "reefPi_RPi_schema"

logger = logging.getLogger(__name__)

def initLogger(logFile):
	logger.setLevel(logging.DEBUG)
	ch = logging.handlers.RotatingFileHandler(
	              logFile, maxBytes=20000, backupCount=5)
	ch.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s:%(filename)25s:%(levelname)7s:%(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)

def findPythonFile(className, rootDir, searchDir):
	relFile = None
	for dirName, subdirList, fileList in os.walk(searchDir):
		#print('Found directory: %s' % dirName)
		for fileName in fileList:
			#logger.info "findPythonFile: checking {0} against {1}".format(os.path.splitext(fileName)[0], className)
			if(os.path.splitext(fileName)[0] == className):
				#logger.info "findPythonFile: found {0} in {1}".format(fileName, dirName)
				relDir = os.path.relpath(dirName, rootDir)
				relFile = os.path.join(relDir, fileName)
				break

		if(relFile != None):
			break

	logger.info("found file = {0} with path = {1}".format(relFile, relDir))
	importPath = os.path.splitext(relFile)[0].replace('/', '.')
	loaded_mod = __import__(importPath, fromlist=[className])
	return getattr(loaded_mod, className)

def createDevice(deviceInfo, DB):
	#get a list of all of the actions for this sensor.  This could be empty
	actionList = []
	device = None
	# get the actions for this sensor
	for action in DB.getAllDeviceActions(deviceInfo['iddevice']):
		actionList.append(deviceAction(action))

	loadedClass = findPythonFile( deviceInfo['deviceTypeName'], '.', './devices')
	return loadedClass(deviceInfo, actionList, DB, logger)

def getAllDevices(DB):
	deviceList = []
	dbDeviceList = DB.getAllDevices()
	for dbDevice in dbDeviceList:
		deviceList.append(createDevice(dbDevice, DB))
	return deviceList

def initDevices(DB):
	devices = getAllDevices(DB)
	for device in devices:
		device.init()

def init(DB):

	addTestData(DB)
	#initDevices(DB)
	scheduledEvents = []
	dbEventList = DB.getAllScheduledEvents()
	for dbEvent in dbEventList:
		logger.info("adding event {0}".format(dbEvent))
		scheduledEvents.append(scheduledEvent(dbEvent))

	return scheduledEvents



#
# put some data in the DB so I have something to play
# with.  This wil be removed when we have data coming
# form he UI
#
def addTestData(DB):
	DB.configure()
	DB.addControllerType('PCAType', 'this is the type to represent the PCA I2C type controller')
	DB.addController('PCA', 'this is the type to represnt the PCA I2C type controller', 1)
	DB.addControllerType('OneWireBus', 'this is the type to represent the one wire bus')
	DB.addController('DIO', 'this is the type to represnt the PCA I2C type controller', 2)


	DB.addDeviceCommand('turnOn', 'turn the device on')
	DB.addDeviceCommand('turnOff', 'turn the device off')
	DB.addDeviceCommand('setOutput', 'set the output value to that given (uses the value entry)')
	DB.addDeviceCommand('getReading', 'get the reading from a sensor type device.  Will automatically \
						 trigger any actions linked to the device depending on the coditions set in the action')

	DB.addBusType('I2C', "standard I2C bus")
	DB.addBusType('SW', "used by represent simulated bus")

	DB.addDeviceType('heaterSimulator', 1)
	DB.addDeviceType('LEDSimulator', 2)

	DB.addDeviceType('tempSensorSimulator', 2)


	DB.addDevice('heater1', 1, '0x40', 0, 1, 0)
	DB.addDevice('LEDFAN', 1, '0x48', 0, 1, 0)
	DB.addDevice('LEDChannel1', 2, '0x4A', 0, 1, 0)
	DB.addDevice('LEDChannel2', 2, '0x4F', 0, 1, 0)
	DB.addDevice('LEDChannel3', 2, '0x50', 0, 1, 0)


	DB.addDeviceActionType('crossing', 'Run the action only once when the condition is met')
	DB.addDeviceActionType('cont', 'Call the action continuously (every period) is the condition is met')
	DB.addDeviceActionRelation('lt', '<', "less than")
	DB.addDeviceActionRelation('gt', '>', "greater than")
	DB.addDeviceActionRelation('eq', '=', "equal to")
	DB.addDeviceActionRelation('neq', '!-', "not equal to")


	# create a temp sensor simulator to represent a tank heater
	DB.addDevice('tempSensor1', 3, 'SW', 1, 1, 0)
	DB.addDeviceAction(6, 25, 1, 1, 1, 1, '')
	DB.addDeviceAction(6, 25, 2, 1, 1, 2, '')

	# create a temp sensor simulator to represent the LED fans
	DB.addDevice('tempSensor2', 3, 'SW', 1, 1, 0)
	DB.addDeviceAction(7, 27, 2, 1, 2, 1, '')
	DB.addDeviceAction(7, 27, 1, 2, 2, 2, '')

	DB.addScheduleType("crone", "crone task based on standard crone syntax")
	DB.addScheduleType("interval", "task will run at regular intervals with period defined here")

	DB.addScheduledEvent("TempSensor1Sample", 2, 6, 4, None, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 5)

	DB.addScheduledEvent("croneEvent", 1, 3, 1, 100, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 6)
	DB.addScheduledEvent("croneEvent", 1, 3, 2, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 36)
	DB.addScheduledEvent("intervalEvent", 2, 4, 2, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 10)
	DB.addScheduledEvent("intervalEvent", 2, 4, 1, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 10)
	DB.addScheduledEvent("intervalEvent", 2, 5, 3, 255, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 2)


#
# Uses the current data time to get the intensity value
# for the lights based on longitude and latitude.
#
def getLEDIntensity():
	return calculateSunLight(BluePWMHigh[0], BluePWMLow[0], BlueFull[0], \
						datetime.datetime.now(), \
						latitude, longitude, \
						TimeZone)

#
# gets the next command from the command table in the
# db and decodes it.  It then calls the command
# on the selected device
#
def processCommand(DB):
	result = None
	command = None

	# check for a command form the DB
	dbCommand = DB.getNextCommand()
	if(dbCommand != None):
		command = deviceCommand(dbCommand)
		logger.info( "running method {0} on device {1}".format(command.deviceCommand, command.deviceName))
		try:
			dbDevice = DB.getDevice(command.iddevice)
			device = createDevice(dbDevice, DB)
			#we have found the device now check it has the correct method
			logger.info( "processCommand: device = {0}".format(device))
			methodPointer = getattr(device, command.deviceCommand, None)
			if(methodPointer):
				# we need to check for parameters and call the method
				# with the correct parameter list. There must be a more
				# generic way of doing this... methodpointer(*command.args) maybe
				paramLength = len(inspect.getargspec(methodPointer)[0])-1
				if(paramLength == 0):
					result = methodPointer()
				elif(paramLength == 1):
					result = methodPointer(command.args)

			else:
				logger.error( "failed to run method {0} on device {1}".format(command.deviceCommand, command.deviceName))

		except Exception, e:
			logger.error( "failed to run method {0} on device {1}: {2}".format(command.deviceCommand, command.deviceName, e))

	return result


def decodeSchedulerEvent(deviceId, probeID, command, level):
	logger.info(":Scheduled event running: " + str(command) +' ' + str(deviceId))
	DB = SQLInterface(host, user, passwd, dataBase, logger)
	DB.addCommand(deviceId, command, [level])



def addScheduledEvents(scheduler, scheduledEvents):
	for event in scheduledEvents:
		if(event.scheduleTypeName == 'crone'):
			scheduler.AddCroneEvent(decodeSchedulerEvent, event)
		elif(event.scheduleTypeName == 'interval'):
			scheduler.AddIntervalEvent(decodeSchedulerEvent, event)


def main():
	scheduledEvents = []
	DB = SQLInterface(host, user, passwd, dataBase, logger)
	scheduledEvents = init(DB)
	scheduler = ReefPI_Scheduler(host, user, passwd, dataBase)
	addScheduledEvents(scheduler, scheduledEvents)
	scheduler.Run()


	#Main loop.  When happy this will be switched to a while(1) or similar
	# for now its easier to limit number of loops
	while(1):
	#for loop in range(1,100):
		while(processCommand(DB)):
			pass
		time.sleep(1)


	logger.info( 'Going to sleep')
	for process in sensorPool:
		process.terminate()

if __name__ == "__main__":
	initLogger('test.log')
	main()
