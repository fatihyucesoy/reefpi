import web
import time
import datetime
import inspect

from DBInterface.SQLInterface import *

from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *

from devices.heater.heaterSimulator import *
from devices.lighting.LEDSimulator import *

from scheduler.reefPI_Scheduler import *

from lib.LEDIntensityCalculator import *
from lib.scheduledEvent import *
from lib.sensorAction import *
from lib.command import *

latitude = -19.770621   # + to N  Defualt - (-19.770621) Heart Reef, Great Barrier Reef, QLD, Australia 
longitude = 149.238532  # + to E  Defualt - (149.238532)
TimeZone = 10             # + to E  Defulat - (10)

host = "localhost"
user = "root"
passwd = ""
dataBase = "reefPi_RPi_schema"
		
def createSensor(sensorInfo, DB):
	#get a list of all of the actions for this sensor.  This could be empty
	actionList = []
	sensor = None
	
	
	# get the actions for this sensor
	for action in DB.getAllSensorActions(sensorInfo['idsensor']):
		actionList.append(sensorAction(action))
	
	
	#create a sensor object of the correct type
	#need to figure out how to make this more generic
	if(sensorInfo['sensorTypeName'] == 'tempSimulator'):
		sensor = tempSimulator(sensorInfo, actionList, host, user, passwd, dataBase)
	elif(sensor['sensorTypeName'] == 'DS18B20'):
		sensor  = DS1882Interface(sensor[1])
		
	return sensor
			
	
def getAllSensors(DB):
	sensorList = []
	# get all sensors from the DB
	dBSensors = DB.getAllSensors()
	# create a sensor object for each DB entry
	for dbSensor in dBSensors:
		sensor = createSensor(dbSensor, DB)
		if(sensor):
			sensorList.append(sensor)
	
	return sensorList

def createDevice(deviceInfo):
	device = None
	if(deviceInfo['deviceTypeName'] == 'heaterSimulator'):
			device = heaterSimulator(deviceInfo, host, user, passwd, dataBase)
	elif(deviceInfo['deviceTypeName'] == 'LEDSimulator'):
			device = LEDSimulator(deviceInfo, host, user, passwd, dataBase)
	return device

def getAllDevices(DB):
	deviceList = []
	dbDeviceList = DB.getAllDevices()
	for dbDevice in dbDeviceList:
		deviceList.append(createDevice(dbDevice))
	return deviceList
		
		
	
		
def init(sensors, sensorPool, devices, scheduledEvents, DB, host, user, passwd, dataBase):
	
	# This should be removed when we get up and running as it
	# recreates the DB
	addTestData(DB)
	
	devices = getAllDevices(DB)
	sensors = getAllSensors(DB)
	#Start the sensors and create the sensorPool
	for sensor in sensors: 
		sensorPool.append(sensor.run())	
		
	dbEventList = DB.getAllScheduledEvents()
	for dbEvent in dbEventList:
		scheduledEvents.append(scheduledEvent(dbEvent))
			


#
# put some data in the DB so I have something to play
# with.  This wil be removed when we have data coming
# form he UI
#
def addTestData(DB):
	DB.configure()
	DB.addControllerType('PCA thingy', 'this is the type to represent the PCA I2C type controller')
	DB.addController('PCA', 'this is the type to represnt the PCA I2C type controller', 1)
	
	DB.addDeviceCommand('turnOn', 'turn the device on')
	DB.addDeviceCommand('turnOff', 'turn the device off')
	DB.addDeviceCommand('setOutput', 'set the output value to that given (uses the value entry)')
	
	
	DB.addDeviceType('heaterSimulator', 'I2C')
	DB.addDeviceType('LEDSimulator', 'I2C')
	DB.addDevice('heater1', 1, '0x40', 0, 1, 0)
	DB.addDevice('LEDFAN', 1, '0x48', 0, 1, 0)
	DB.addDevice('LEDChannel1', 2, '0x4A', 0, 1, 0)
	DB.addDevice('LEDChannel2', 2, '0x4F', 0, 1, 0)
	DB.addDevice('LEDChannel3', 2, '0x50', 0, 1, 0)
	
	
	DB.addSensorType('tempSimulator', 'SW')
	DB.addSensorActionType('crossing', 'Run the action only once when the condition is met')
	DB.addSensorActionType('cont', 'Call the action continuously (every period) is the condition is met')
	DB.addSensorActionRelation('lt', '<', "less than")
	DB.addSensorActionRelation('gt', '>', "greater than")
	DB.addSensorActionRelation('eq', '=', "equal to")
	DB.addSensorActionRelation('neq', '!-', "lnot equal to")
	# create a temp sensor simulator to represent a tank heater
	DB.addSensor('tempSensor1', 1, 'SW', 'degrees', 3)
	DB.addSensorAction(1, 25, 1, 1, 1, 1)
	DB.addSensorAction(1, 25, 2, 1, 1, 2)
	
	# create a temp sensor simulator to represent the LED fans
	DB.addSensor('tempSensor2', 1, 'SW', 'celcius', 4)
	DB.addSensorAction(2, 27, 2, 1, 2, 1)
	DB.addSensorAction(2, 27, 1, 2, 2, 2)
	
	DB.addScheduleType("crone", "crone task based on standard crone syntax")
	DB.addScheduleType("interval", "task will run at regular intervals with period defined here")
	
	
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
	dBCommand = DB.getNextCommand()
	if(dBCommand != None):
		command = deviceCommand(dBCommand)
		print "running method {0} on device {1}".format(command.deviceCommand, command.deviceName)
		try:
			dbDevice = DB.getDevice(command.iddevice)
			device = createDevice(dbDevice)
			#we have found the device now check it has the correct method
			methodPointer = getattr(device, command.deviceCommand, None)
			if(methodPointer):
				# we need to check for parameters and call the method
				# with the correct parameter list. There must be a more
				# generic way of doing this... methodpointer(*command.args) maybe
				paramLength = len(inspect.getargspec(methodPointer)[0])-1
				if(paramLength == 0):
					result = methodPointer()
				elif(paramLength == 1):
					result = methodPointer(command.args[0])
				
			else:
				print "failed to run method {0} on device {1}".format(command.deviceCommand, command.deviceName)
			
		except Exception, e:
			print "failed to run method {0} on device {1}: {2}".format(command.deviceCommand, command.deviceName, e)
			
	return result

		
def decodeSchedulerEvent(deviceId, probeID, command, level):
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + \
			":Scheduled event running: " + str(command) +' ' + str(deviceId)	
	DB = SQLInterface(host, user, passwd, dataBase)
	DB.addCommand(deviceId, command, [level])



def addScheduledEvents(scheduler, scheduledEvents):
	for event in scheduledEvents:
		if(event.scheduleTypeName == 'crone'):
			scheduler.AddCroneEvent(decodeSchedulerEvent, event)
		elif(event.scheduleTypeName == 'interval'):
			scheduler.AddIntervalEvent(decodeSchedulerEvent, event)

#
# 
#
#
def checkForSystemUpdates(sensors, sensorPool,  devices, scheduledEvents, DB):
	sensor = sensors
	
def main():

	sensors = []
	devices = []
	sensorPool = []
	scheduledEvents = []
	DB = SQLInterface(host, user, passwd, dataBase)
	#I am not sure about this anymore... I might just create instances when I need them
	#this might avoid the need to resync with the DB to check for changes........
	# will have to do lot more error checking on the calls.. also wonder if its worth just 
	#setting up an interval event to cover the sensors
	#we probably just want to use the init to set everything to the state defined in the DB.
	#this takes care of initial state
	init(sensors, sensorPool,  devices, scheduledEvents, DB, host, user, passwd, dataBase)

	scheduler = ReefPI_Scheduler(host, user, passwd, dataBase)
	addScheduledEvents(scheduler, scheduledEvents)
	scheduler.Run()

	
	#Main loop.  When happy this will be switched to a while(1) or similar
	# for now its easier to limit number of loops
	while(1):
	#for loop in range(1,100):
		while(processCommand(DB)):
			pass
			
		#TODO scan the db for changes such as new devices or events
		checkForSystemUpdates(sensors, sensorPool,  devices, scheduledEvents, DB)
		time.sleep(1)
	
	
	print 'Going to sleep'	
	for process in sensorPool:
		process.terminate()


if __name__ == "__main__":
    main()
