import magum
import pickle 

magum = magum.Magum(250,0,4,1)

# Calibrating the sensors and saving them to cal file.
cal_sens = magum.calibrateSens(1000)
print(cal_sens)
pickle.dump(cal_sens, open('cal','wb'))

