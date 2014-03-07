import web
import time


from DBInterface.SQLiteInterface import *
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
	DB     = SQLiteInterface()
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
	DB     = SQLiteInterface()
	DB.createDateBase()
	DB.addSensor('tempSensor1', 'tempSimulator', 'sw', 25.5, 25.5, 'heater1')
	#DB.addSensor('simulator2', 'tempSimulator', 'sw')
	#DB.addSensor('simulator3', 'tempSimulator', 'sw')
	#DB.addSensor('simulator4', 'tempSimulator', 'sw')
	DB.addDevice('heater1', 'heaterSimulator', 'sw')
	
def processCommand(devices):
	result = None
	DB     = SQLiteInterface()
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
	DB     = SQLiteInterface()
	
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

			
def main():
	tempProbes = []
	devices = []	
	configureDB()
	init(tempProbes, devices)
	
	#mainloop
	for i in range(1,100):
		#process the next command in the DB
		processCommand(devices)
		processTempProbes(tempProbes)
		time.sleep(1)
		
		
	DB     = SQLiteInterface()	
	rows = DB.getAllTemperatures()	
	for row in rows:
		print row

	
	

	
	

if __name__ == "__main__":
    main()
