import magum
import pickle
import zmq
import time

###############
#Initialization
###############
#Sensors object
magum = magum.Magum(2000,0,2,1)

#Zmq-communications
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind('tcp://10.42.0.114:9876')

#The calibration values are calculated with 1000 samples in the
#file 'cal'. calibrateSens function also run for internal reasons.

cal_sens = magum.calibrateSens(1)
cal_sens = pickle.load(open('cal','rb'))


#Read angle values for x[0], y[1], z[2] axes and send data with zmq.
cal_acc_gyr = cal_sens[0:6]
dt = 0.1

while True:
	angles_array = magum.compFilter(dt,cal_acc_gyr)
	compFiltObj = (time.time(),angles_array)
	publisher.send_pyobj(compFiltObj)
	print 'x {}'.format(angles_array[0])
	print 'y {}'.format(angles_array[1])
	print 'z {}'.format(angles_array[2])


