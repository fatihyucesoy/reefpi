# This is a python port of the following:
# Natural Reef Aquarium Lighting V2.5.6
# 30/11/2013
# Developed by J. Harp (nUm - RTAW Forums, Numlock10 - Reef Central Forums)
# Formulas based off of information from NOAA website for sunrise / sunset times.
# Includes Lunar Simulation.
from math import *

blueChannels = 1    # how many PWMs for blues (count from above)
whiteChannels = 1    # how many PWMs for whites (count from above)
uvChannels = 1    # how many PWMs for uv (count from above)
moonChannels = 1    # how many PWMs from moon (count from above)

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

latitude1 = -19.770621   # + to N  Defualt - (-19.770621) Heart Reef, Great Barrier Reef, QLD, Australia 
longitude1 = 149.238532  # + to E  Defualt - (149.238532)
TimeZone1 = 10             # + to E  Defulat - (10)

# Sunlight Variables

delayTime = 0     # start time delay in minutes,  - will push the day back, + will bring the day forward

def Map(x, in_min, in_max, out_minute, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def calculateSunLight(_ledHigh, _ledLow, _fullSun, _datetime, _latitude, _longitude, _timeZone):
	
	a = floor((14.0 - _datetime.month) / 12.0)
	y = _datetime.year + 4800.0 - a
	m = _datetime.month + (12.0 * a) - 3.0
	
	JC = (((_datetime.day + floor(((153.0 * m) + 2.0) / 5.0) + (365.0 * y) + floor(y / 4.0) - floor(y / 100.0) + floor(y / 400.0) - 32045.0) + (float(_datetime.hour / 24.0) + (_datetime.minute / 1444.0) + (_datetime.second / 86400.0))) - 2451556.08) / 36525.0
	
	GMLS = fmod(280.46646 + JC*(36000.76983 + JC * 0.0003032), 360.0)
	GMAS = 357.52911 + JC * (35999.05029 - 0.0001537 * JC)
	EEO = 0.016708634 - JC * (0.000042037 + 0.0000001267 * JC)
	SEoC = sin((GMAS * pi) / 180.0)*(1.914602 - JC * (0.004817 + 0.000014 * JC)) + sin(((2.0 * GMAS) * pi) \
			 / 180.0) * (0.019993 - 0.000101 * JC) + sin(((3.0 * JC) * pi) / 180.0) * 0.000289
	STL = GMLS + SEoC
	STA = GMAS + SEoC
	SRV = (1.000001018 * (1.0 - EEO * EEO)) / (1.0 + EEO * cos((STA * pi) / 180.0))
	SAL = STL - 0.00569 - 0.00478 * sin(((125.04 - 1934.136 * JC) * pi) / 180.0)
	MOE = 23.0 + (26.0 + ((21.448 - JC * (46.815 + JC * (0.00059 - JC * 0.001813)))) / 60.0) / 60.0
	OC = MOE + 0.00256 * cos(((215.04 - 1934.136 * JC) * pi) / 180.0)
	SD = (asin(sin((OC * pi) / 180.0) * sin((SAL * pi) / 180.0))) * (180.0 / pi)
	vy = tan(((OC / 2.0) * pi) / 180.0) * tan(((OC / 2.0) * pi) / 180.0)
	EQoT = (4.0 * (vy * (sin(2.0 * ((GMLS * pi) / 180.0)) - 2.0 * EEO * sin((GMAS * pi) / 180.0) \
			 + 4.0 * EEO * vy * sin((GMAS * pi) / 180.0) * cos(2.0 * ((GMLS * pi) / 180.0)) \
			 - 0.5 * vy * vy * sin(4.0 * ((GMLS * pi) / 180.0)) - 1.25 * EEO * EEO * \
			 sin(2 * ((GMAS * pi) / 180))))) * (180 / pi);
	HAS = acos(cos((90.833 * pi) / 180.0) / (cos((_latitude * pi) / 180.0) * cos((SD * pi) / 180.0)) \
			- tan((_latitude * pi) / 180.0) * tan((SD * pi) / 180.0)) * (180.0 / pi)
	SN = (720.0 - 4.0 * _longitude - EQoT + _timeZone * 60.0)
	SR = SN - HAS * 4.0
	SS = SN + HAS * 4.0
	STD = 8.0 * HAS
	TST = fmod((((_datetime.hour)+(_datetime.minute / 60.0) + (_datetime.second / 3600.0)) / 24.0) * 1440.0 + EQoT + 4.0 * _longitude - 60.0 * \
			 _timeZone, 1440.0) + delayTime

	if (TST / 4 < 0.0):
		AH = ((TST / 4.0) + 180.0)
	else:
		AH = ((TST / 4.0) - 180.0)
	
	SZA = (acos(sin((_latitude * pi) / 180.0) * sin((SD * pi) / 180.0) + cos((_latitude * pi) \
		/ 180.0) * cos((SD * pi) / 180.0) * cos((AH * pi) / 180.0))) * (180.0 / pi)
	
	SEA = 90.0 - SZA
	
	if (SEA <= 0.0):
		result = _ledLow
	elif(SEA < _fullSun):
		result = Map(SEA, 0, _fullSun, _ledLow, _ledHigh)
	else:
		result = _ledHigh
		
	return result

def MoonLight(_ledPin,  _ledHigh,  _ledLow,  _datetime):

	a = floor((14.0 - _datetime.month) / 12.0)
	y = _datetime.year + 4800.0 - a
	m = _datetime.month + (12.0 * a) - 3.0
	
	mJDN = ((_datetime.day  + ((153.0 * m + 2.0) / 5.0) + (365.0 * y) + (y / 4.0) - ( y / 100.0) + (y / 400.0) - 32045.0) + 730483.71)

	mJDR = (_datetime.hour / 24.0) + (_datetime.minute / 1444.0) + (_datetime.second / 86400.0)

	mJD = mJDN + mJDR
	
	moon = fmod((mJD - 2456318.69458333), 29.530589)
	
	if (moon < 14.7652945):
		result = Map(moon, 0.0, 14.7652945, _ledHigh, _ledLow)
	else:
		result = Map(moon, 14.7652946, 29.530589, _ledLow, _ledHigh)
	
	return result







#value = SunLight(bluePins[i], BluePWMHigh[i], BluePWMLow[i], BlueFull[i], year, month, dayOfMonth, rtcHrs, rtcMins, second)