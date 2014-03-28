import web
import time


from DBInterface.SQLiteInterface import *
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
import logging
logging.basicConfig()

#set standalone to false to allow the scheduler to launch in another thread


class ReefPI_Scheduler:

	_host = "localhost"
	_user = "root"
	_passwd = ""
	_dataBase = "reefPi_RPi_schema"	
	_sched = None

	
	def __init__(self,  host, user, passwd, dataBase):
		self._host = host
		self._user = user
		self._passwd = passwd
		self._dataBase = dataBase
		connectString=""
		if(self._passwd!=""):
			connectString = "mysql://"+self._user+":"+self._passwd+"@"+self._host+"/"+self._dataBase
		else:
			connectString = "mysql://"+self._user+"@"+self._host+"/"+self._dataBase
			
		_g_aps_default_config = {'apscheduler.standalone' : False, 
				'apscheduler.jobstore.default.class' : 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore',
    			'apscheduler.jobstore.default.url' : connectString,
    			'apscheduler.jobstore.default.tablename' : 'reefPiSchedulerJobStore'}
    			
		self._sched = Scheduler(_g_aps_default_config)
		  
	def AddIntervalEvent(self, methodPointer, event):
		
		if(event.hour==None):
			hour = 0
		else:
			hour=event.hour
			
		if(event.minute==None):
			minute = 0
		else:
			minute = event.minute
		
		if(event.second==None):
			second = 0
		else:
			second = event.second
			
		if(event.startDate==None):
			startDate = '2013-08-06 00:09:12'
		else:
			startDate = event.startDate
						
		return self.AddIntervalTask(methodPointer, hrs=hour, min=minute, sec=second, \
								startDate=startDate, argList=[event.deviceId, None, event.state, None])
	
	
	
	def AddIntervalTask(self, methodPointer, weeks=0, days=0, hrs=0, min=0, sec=0, startDate='2013-08-06 00:09:12', argList=[]):
		return self._sched.add_interval_job(methodPointer, weeks=weeks, days=days, hours=hrs, minutes=min, seconds=sec, \
											start_date=startDate, args=argList)
											
											
	def AddCroneEvent(self, methodPointer, event):
		return self.AddCroneTask(methodPointer, year=event.year, month=event.month, day=event.day, week=event.week, \
								day_of_week=event.day_of_week, min=event.minute, sec=event.second, hour=event.hour, \
								argList=[event.deviceId, None, event.state, None])

	def AddCroneTask(self, methodPointer, year=None, month=None, day=None, week=None, \
					 day_of_week=None, hour=None, min=None, sec=None, argList=['crone task running']):
		return self._sched.add_cron_job(methodPointer, year, month, day, week, day_of_week, hour, min, sec, args=argList)
			
	def RemoveTask(self, job):
		self._sched.unschedule_job(job)
		
	def Run(self):
		self._sched.start()  
		
