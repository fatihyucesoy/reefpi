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

BluePWMHigh = [ 255, 255 ]        # High value for Blue PWM each vale is for each string - if your values are noraml this is 255, if your values are inverted this is 0
BluePWMLow = [ 0, 0 ]            # Low value for Blue PWM - if your values are noraml this is 0, if your values are inverted this is 255
BlueFull = [ 25, 25 ]          # Value in degrees (sun angle) that each Blue string will be at max output (Larger = more sunlight)
WhitePWMHigh = [ 255, 255 ]        # High value for White PWM - if your values are noraml this is 255, if your values are inverted this is 0
WhitePWMLow = [ 0, 0 ]            # Low value for White PWM - if your values are noraml this is 0, if your values are inverted this is 255
WhiteFull = [ 37.5, 37.5 ]      # Value in degrees (sun angle) that each White string will be at max output (Larger = more sunlight)
UVPWMHigh = [ 255 ]             # High value for UV PWM - if your values are noraml this is 255, if your values are inverted this is 0
UVPWMLow = [ 0 ]               # Low value for UV PWM - if your values are noraml this is 0, if your values are inverted this is 255
UVFull = [ 30 ]              # Value in degrees (sun angle) that each UV string will be at max output (Larger = more sunlight)
MoonPWMHigh = [ 255 ]             # High value for Moon PWM - if your values are noraml this is 255, if your values are inverted this is 0
MoonPWMLow = [ 0 ]               # Low value for Moon PWM - if your values are noraml this is 0, if your values are inverted this is 255

# Set for the location of the world you want to replicate.

latitude = -19.770621   # + to N  Defualt - (-19.770621) Heart Reef, Great Barrier Reef, QLD, Australia 
longitude = 149.238532  # + to E  Defualt - (149.238532)
TimeZone = 10             # + to E  Defulat - (10)


#commandDict={1:turnHeaterOn, 2:turnHeaterOff}

#def _getCommandID(searchCommand):
#	returnValue = 0
		
#	for Id, command in commandDict.items():
#		if command == searchCommand:
#			returnValue = Id
#			break
#		
#	return returnValue
	
		
def init(sensors, devices):
	DB     = SQLInterface()
	configureDB()
	DBSensors = DB.getAllSensors()
	for sensor in DBSensors:
		if(DB.getSensorType(sensor[2]) == 'tempSimulator'):
			sensors.append(tempSimulator(sensor[0], sensor[1], sensor[4], sensor[5], sensor[6], sensor[7]))
		elif(sensor[2] == 'DS18B20'):
			sensors.append(DS1882Interface(sensor[1]))

	dbDevices = DB.getAllDevices()
	for device in dbDevices:
		if(DB.getDeviceType(device[2]) == 'heaterSimulator'):
			devices.append(heaterSimulator(device[0], device[1], device[2], device[3]))
		elif(DB.getDeviceType(device[2]) == 'LEDSimulator'):
			devices.append(LEDSimulator(device[0], device[1], device[2], device[3]))

def configureDB():
	DB     = SQLInterface()
	DB.config();
	#DB.createDateBase()
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

def getLEDIntensity():
	return calculateSunLight(BluePWMHigh[0], BluePWMLow[0], BlueFull[0], \
						datetime.datetime.now(), \
						latitude, longitude, \
						TimeZone)	
	
def processCommand(devices):
	result = None
	DB     = SQLInterface()
	command = DB.getNextCommand()
	if(command[0] != None):
	
		#get the device with the correct device ID
		for device in devices:
			if(device.getId() == int(command[1])):
				print 'storing'
				cmdDevice = device
				break
					
		if(command[0] == 1):
			result = cmdDevice.turnDeviceOn()
		elif(command[0] == 2):
			result = cmdDevice.turnDeviceOff()
		elif(command[0] == 3):
			result = cmdDevice.setIntensity(command[2])	
		
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
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ":Scheduled event running: " + str(commandId) +' ' + str(deviceId)	
	DB     = SQLInterface()

	if(commandId=='1'):
		DB.addCommand(commandId, deviceId)
	elif(commandId=='2'):
		DB.addCommand(commandId, deviceId)
	elif(commandId=='3'):
		DB.addCommand(commandId, deviceId, level)

	
def main():
	sensors = []
	devices = []
	sensorPool = []
		
	init(sensors, devices)

	scheduler = ReefPI_Scheduler()
	scheduler.AddIntervalTask(decodeSchedulerEvent, \
										min=0, sec=5, hrs=0, \
										startDate= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
										argList=['1', None,'1', None])
	scheduler.AddIntervalTask(decodeSchedulerEvent, \
										min=0, sec=5, hrs=0, \
										startDate= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
										argList=['3',None, '3', 10,])
										
	#scheduler a task to run at 5 seconds past every minute
	scheduler.AddCroneTask(decodeSchedulerEvent, \
										sec=5,\
										startDate= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
										argList=['2', None,'1', None])
	scheduler.Run()
	
	
	
	# creates a separate process for each sensor to run it
	# this allows them to be independent.
	for sensor in sensors: 
		process = Process(target=processSensor, args=(sensor,))
		process.start()
		sensorPool.append(process)		
	
	#Main loop.  When happy this will be switched to a while(1) or similar
	# for now its easier to limit number of loops
	for loop in range(1,100):
		processCommand(devices)
		lightlevel = calculateSunLight(BluePWMHigh[0], BluePWMLow[0], BlueFull[0], \
										datetime.datetime.now(), \
										latitude, longitude, TimeZone)
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': and all is well :' + str(lightlevel)
		time.sleep(1)
		
	print 'Going to sleep'	
	for process in sensorPool:
		process.terminate()


if __name__ == "__main__":
    main()
