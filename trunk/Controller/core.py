import web
import time
import datetime
from multiprocessing import Process

from DBInterface.SQLInterface import *

from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *

from devices.heater.heaterSimulator import *
from devices.lighting.LEDSimulator import *

from scheduler.reefPI_Scheduler import *

from lib.LEDIntensityCalculator import *
from lib.scheduledEvent import *

latitude = -19.770621   # + to N  Defualt - (-19.770621) Heart Reef, Great Barrier Reef, QLD, Australia 
longitude = 149.238532  # + to E  Defualt - (149.238532)
TimeZone = 10             # + to E  Defulat - (10)

host = "localhost"
user = "root"
passwd = ""
dataBase = "reefPi_RPi_schema"
	
def init(sensors, devices, scheduledEvents, DB, host, user, passwd, dataBase):
	configureDB(DB)
	
	DBSensors = DB.getAllSensors()
	for sensor in DBSensors:
		if(DB.getSensorType(sensor[2]) == 'tempSimulator'):
			sensors.append(tempSimulator(sensor[0], sensor[1], sensor[4], sensor[5], sensor[6], sensor[7], \
							host, user, passwd, dataBase))
		elif(sensor[2] == 'DS18B20'):
			sensors.append(DS1882Interface(sensor[1]))

	dbDevices = DB.getAllDevices()
	for device in dbDevices:
		if(DB.getDeviceType(device[2]) == 'heaterSimulator'):
			devices.append(heaterSimulator(device[0], device[1], device[2], device[3], \
							host, user, passwd, dataBase))
		elif(DB.getDeviceType(device[2]) == 'LEDSimulator'):
			devices.append(LEDSimulator(device[0], device[1], device[2], device[3], \
							host, user, passwd, dataBase))
			
	dbEvents = DB.getAllScheduledEvents()
	for event in dbEvents:
		scheduledEvents.append(scheduledEvent(event))
			


#
# put some data in the DB so I have something to play
# with.  This wil be removed when we have data coming
# form he UI
#
def configureDB(DB):
	DB.configure()
	DB.addControllerType('PCA thingy', 'this is the type to represnt the PCA I2C type controller')
	DB.addController('PCA', 'this is the type to represnt the PCA I2C type controller', 1)
	DB.addDeviceType('heaterSimulator', 'I2C')
	DB.addDeviceType('LEDSimulator', 'I2C')
	DB.addDevice('heater1', 1, '0x40', 0, 1, 0)
	DB.addDevice('heater2', 1, '0x48', 0, 1, 0)
	DB.addDevice('LEDChannel1', 2, '0x4A', 0, 1, 0)
	DB.addDevice('LEDChannel2', 2, '0x4F', 0, 1, 0)
	DB.addDevice('LEDChannel3', 2, '0x50', 0, 1, 0)
	DB.addSensorType('tempSimulator', 'SW')
	DB.addSensor('tempSensor1', 1, '4', 25.5, 25.5, 1, 3)
	DB.addSensor('tempSensor2', 1, '5', 25.5, 25.5, 2, 4)
	DB.addScheduledEvent("croneEvent", "crone", 1, 1, 100, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 6)
	DB.addScheduledEvent("intervalEvent", "interval", 2, 0, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
						 None, None, None, None, None, None, None, 3)	



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
def processCommand(devices, DB):
	result = None
	command = DB.getNextCommand()
	if(command[0] != None):
	
		#get the device with the correct device ID
		for device in devices:
			if(device.getId() == int(command[1])):
				cmdDevice = device
				break
					
		if(command[0] == 1):
			result = cmdDevice.turnDeviceOn()
		elif(command[0] == 2):
			result = cmdDevice.turnDeviceOff()
		elif(command[0] == 3):
			result = cmdDevice.setIntensity(command[1])	
		
	return result
		

# Function loops until killed by the calling process.
# Intended to be launched as a separate process.  Takes
# the sensor object as requests get reading. Then sleeps for 
# the defined period
def processSensor(sensor):
	while(1):
		reading = sensor.takeNewReading()
		print 'Probe:' + str(sensor.getProbeId()) + ' current temp is:' + str(reading)	 	
		time.sleep(int(sensor.getPeriod()))
		
		

def decodeSchedulerEvent(commandId, probeID, deviceId, level):
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + \
			":Scheduled event running: " + str(commandId) +' ' + str(deviceId)	
	DB = SQLInterface(host, user, passwd, dataBase)
	if(commandId=='1'):
		DB.addCommand(commandId, deviceId)
	elif(commandId=='2'):
		DB.addCommand(commandId, deviceId)
	elif(commandId=='3'):
		DB.addCommand(commandId, deviceId)


#
#
#
def addScheduledEvents(scheduler, scheduledEvents):
	for event in scheduledEvents:
		if(event.type == 'crone'):
			scheduler.AddCroneEvent(decodeSchedulerEvent, event)
		elif(event.type == 'interval'):
			scheduler.AddIntervalEvent(decodeSchedulerEvent, event)


#
# creates a separate process for each sensor to run it
# this allows them to be independent.
#										
def createSensors(sensorPool, sensors):
	for sensor in sensors: 
		process = Process(target=processSensor, args=(sensor,))
		process.start()
		sensorPool.append(process)	


	
def main():

	sensors = []
	devices = []
	sensorPool = []
	scheduledEvents = []
	DB = SQLInterface(host, user, passwd, dataBase)
		
	init(sensors, devices, scheduledEvents, DB, host, user, passwd, dataBase)
	createSensors(sensorPool, sensors)
	
	scheduler = ReefPI_Scheduler(host, user, passwd, dataBase)
	addScheduledEvents(scheduler, scheduledEvents)
	scheduler.Run()

	
	#Main loop.  When happy this will be switched to a while(1) or similar
	# for now its easier to limit number of loops
	while(1):
	#for loop in range(1,100):
		processCommand(devices, DB)
		#TODO scan the db for changes such as new devices or events
		time.sleep(1)
	
	
	print 'Going to sleep'	
	for process in sensorPool:
		process.terminate()


if __name__ == "__main__":
    main()