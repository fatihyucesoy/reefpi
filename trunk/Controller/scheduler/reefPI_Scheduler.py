import web
import time


from DBInterface.SQLiteInterface import *
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.sqlalchemy_store import SQLAlchemyJobStore
import logging
logging.basicConfig()

#set standalone to false to allow the scheduler to launch in another thread
_g_aps_default_config = {
    'apscheduler.standalone' : False,
    'apscheduler.jobstore.default.class' : 'apscheduler.jobstores.sqlalchemy_store:SQLAlchemyJobStore',
    'apscheduler.jobstore.default.url' : 'mysql://root@localhost/reefPi_RPi_schema',
    'apscheduler.jobstore.default.tablename' : 'reefPiSchedulerJobStore'
}


class ReefPI_Scheduler:
	_sched = None
	
	def __init__(self):
		self._sched = Scheduler(_g_aps_default_config)
		  
		
	def AddIntervalTask(self, methodPointer, min=0, sec=0, hrs=0, startDate='2013-08-06 00:09:12', argList=['Interval task running']):
		print argList
		return self._sched.add_interval_job(methodPointer, minutes=min, seconds=sec, hours=hrs, start_date=startDate, args=argList)

	def AddCroneTask(self, methodPointer, min=None, sec=None, hrs=None, startDate='2013-08-06 00:09:12', argList=['crone task running']):
		return self._sched.add_cron_job(methodPointer, year=None, month=None, day=None, week=None, day_of_week=None, hour=hrs, minute=min, second=sec, args=argList)
			
	def RemoveTask(self, job):
		self._sched.unschedule_job(job)
		
	def Run(self):
		self._sched.start()  
		
