import os
import glob

class DS1882Interface:
	probeID = 'NONE'
	w1devicefile = None
	
	def __init__(self, probeID):
		self.probeID=probeID
		# enable kernel module
		os.system('sudo modprobe w1-gpio')
		os.system('sudo modprobe w1-therm')
		devicelist = glob.glob('/sys/bus/w1/devices/28*')
		self.w1devicefile = devicelist[0] + '/w1_slave'


	# get temerature
	# returns None on error, or the temperature as a float
	def getTemp(self):
		try:
			fileobj = open(self.w1devicefile,'r')
			lines = fileobj.readlines()
			fileobj.close()
		except:
			return None

    	# get the status from the end of line 1 
		status = lines[0][-4:-1]

    	# is the status is ok, get the temperature from line 2
		if status=="YES":
			tempstr= lines[1][-6:-1]
			return [self.probeID, float(tempstr)/1000]
		else:
			return None

