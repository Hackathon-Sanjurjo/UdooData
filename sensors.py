import magum
import pickle
import zmq
import time

###############
#Initialization
###############
#Sensors object
# gyroscope: 250 gps, accelerometer:+/- 4g 
magum = magum.Magum(250,0,4,1)

#Zmq-communications
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind('tcp://10.42.0.114:9876')

##############
#Calculations
##############
#The calibration values are calculated with 1000 samples in the
#file 'cal'. calibrateSens function is also invoked for internal library 
#reasons.

cal_sens = magum.calibrateSens(1)
cal_sens = pickle.load(open('cal','rb'))
cal_acc_gyr = cal_sens[0:6]
dt = 0.05

while True:
	# Get Data: degrees and acceleration
	angles_array = magum.compFilter(dt,cal_acc_gyr)
	accel_array = magum.readAData('raw') #g force unit
	
	# Send data
	sensorObj = (time.time(),angles_array, accel_array)	
	publisher.send_pyobj(sensorObj)
	print 'x accel {}'.format(accel_array[0])
	print 'x comp {}'.format(angles_array[0])
