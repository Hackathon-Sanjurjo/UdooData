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
with open('.ipconfig') as f:
	ipconfig = f.readlines()[0].strip()
publisher.bind(ipconfig)

#Filter initialization
N = 6
xyz_angles = [[0]*N, [0]*N, [0]*N]
xyz_accel = [[0]*N, [0]*N, [0]*N]

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
	anglesComp_array = magum.compFilter(dt,cal_acc_gyr)
	accel_array = magum.readAData('raw') #g force unit
	angles_array = magum.readGData('raw')
	# Filter Data	
	for i in range(3):
                l = xyz_angles[i]	
		l.append(anglesComp_array[i])
		l.pop(0)
		anglesComp_array[i]= sum(l)/len(l)
	for i in range(3):
		l = xyz_accel[i]
                l.append(accel_array[i])
                l.pop(0)
                accel_array[i]= sum(l)/len(l)
	# Send data
	sensorObj = (time.time(),anglesComp_array, accel_array, 
		angles_array)	
	publisher.send_pyobj(sensorObj)
	print 'Sending data'
