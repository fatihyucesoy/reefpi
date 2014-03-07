import web
import time
from multiprocessing import Process


from DBInterface.SQLInterface import *
from sensors.tempSensor.tempSensorSimulator import *
from sensors.tempSensor.DS18B20Interface import *
from devices.heater.heaterSimulator import *



#commandDict={1:turnHeaterOn, 2:turnHeaterOff}

#def _getCommandID(searchCommand):
#	returnValue = 0
		
#	for Id, command in commandDict.items():
#		if command == searchCommand:
#			returnValue = Id
#			break
#		
#	return returnValue
	
		
def init(tempProbes, devices):
	DB     = SQLInterface()
	configureDB()
	sensors = DB.getAllSensors()
	for sensor in sensors:
		if(sensor[2] == 'tempSimulator'):
			tempProbes.append(tempSimulator(sensor[1], sensor[4], sensor[5], sensor[6]))
		elif(sensor[2] == 'DS18B20'):
			tempProbes.append(DS1882Interface(sensor[1]))

	dbDevices = DB.getAllDevices()
	for device in dbDevices:
		if(device[2] == 'heaterSimulator'):
			devices.append(heaterSimulator())

def configureDB():
	DB     = SQLInterface()
	DB.config();
	#DB.createDateBase()
	DB.addSensor('tempSensor1', 'tempSimulator', 'sw', 25.5, 25.5, 1)
	DB.addSensor('tempSensor2', 'tempSimulator', 'sw', 25.5, 25.5, 2)	
	DB.addDevice('heater1', 'heaterSimulator', 'sw')
	
def processCommand(devices):
	result = None
	DB     = SQLInterface()
	commandId = DB.getNextCommand()
	
	#if(commandId != None):
	#	result = commandDict[commandId]()

	if(commandId == 1):
		#this is turn heater on.  The parameter tells us
		#which heater to switch
		result = devices[0].turnHeaterOn()
		#TODO write the heater state to the DB.
	elif(commandId == 2):
		#this is turn heater on.  The parameter tells us
		#which heater to switch
		result = devices[0].turnHeaterOff()	
		
	return result
	
def processTempProbes(tempProbes):
	DB     = SQLInterface()
	
	for tempProbe in tempProbes:
		temp = tempProbe.getTemp()
		DB.insertSensorReading(tempProbe.getProbeID(), temp)
		print 'Probe:' + tempProbe.getProbeID() + ' current temp is:' + str(temp)
		
		if(temp < tempProbe.getMinTemp()):
			#DB.turnHeaterOn(_getCommandID(turnHeaterOn))
			DB.turnHeaterOn(1)
		else:
			#DB.turnHeateroff(_getCommandID(turnHeaterOff))
			DB.turnHeateroff(2)		

def processSensor(sensor, period):
	DB     = SQLInterface()
	print 'running function - ' + sensor.getProbeID() + ' with period ' + str(period)
	while(1):
		time.sleep(period)
		reading = sensor.getTemp()
		DB.insertSensorReading(sensor.getProbeID(), reading)
		print 'Probe:' + sensor.getProbeID() + ' current temp is:' + str(reading)
		
		if(reading < sensor.getMinTemp()):
			#DB.turnHeaterOn(_getCommandID(turnHeaterOn))
			DB.turnHeaterOn(1)
		else:
			#DB.turnHeateroff(_getCommandID(turnHeaterOff))
		 	DB.turnHeateroff(2)	
			
def main():
	sensors = []
	devices = []
	sensorPool = []
		
	configureDB()
	init(sensors, devices)
		
	print "Waiting for result..."
	i = 1
	for sensor in sensors: # then kill them all off
		process = Process(target=processSensor, args=(sensor, i))
		process.start()
		sensorPool.append(process)
		i+=1
		
		
		
	time.sleep(10)
	
	
	print 'DIE god damn you'
	
	for process in sensorPool:
		process.terminate()
		
	#mainloop
	#for i in range(1,100):
		#process the next command in the DB
	#	processCommand(devices)
	#	processTempProbes(tempProbes)
	#	time.sleep(1)
		
		
	#DB     = SQLiteInterface()	
	#rows = DB.getAllTemperatures()	
	#for row in rows:
		#print row

	
	

	
	

if __name__ == "__main__":
    main()
