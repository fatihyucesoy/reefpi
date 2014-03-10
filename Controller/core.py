import web
import time
import datetime
from multiprocessing import Process


from DBInterface.SQLInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *

from scheduler.reefPI_Scheduler import *



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

def configureDB():
	DB     = SQLInterface()
	DB.config();
	#DB.createDateBase()
	DB.addDeviceType('heaterSimulator', 'I2C')
	DB.addDevice('heater1', 1, '0x40', 0)
	DB.addDevice('heater2', 1, '0x48', 0)
	DB.addSensorType('tempSimulator', 'SW')
	DB.addSensor('tempSensor1', 1, '4', 25.5, 25.5, 1, 3)
	DB.addSensor('tempSensor2', 1, '5', 25.5, 25.5, 2, 4)	

	
	
def processCommand(devices):
	result = None
	DB     = SQLInterface()
	command = DB.getNextCommand()
	if(command[0] != None):
	#result = commandDict[commandId]()
	
		for device in devices:
			if(device.getId() == command[1]):
				break
			
		if(command[0] == 1):
			result = device.turnDeviceOn()
		elif(command[0] == 2):
			result = device.turnDeviceOff()	
		
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
		
def schedulertest(text):
	print "Scheduled event running: " + text	
	
	
def main():
	sensors = []
	devices = []
	sensorPool = []
		
	init(sensors, devices)

	scheduler = ReefPI_Scheduler()
	scheduler.AddIntervalTaskMinutes(schedulertest, min=0, sec=5, hrs=0, startDate= datetime.date.today().strftime("%Y-%m-%d %H:%M:%S"))
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
		print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': and all is well'
		time.sleep(1)
		
	print 'Going to sleep'	
	for process in sensorPool:
		process.terminate()


if __name__ == "__main__":
    main()
