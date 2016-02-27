import magum
import pickle 

magum = magum.Magum(2000,0,2,1)

# Calibrating the sensors and saving them to fcal file.
cal_sens = magum.calibrateSens(1000)
print(cal_sens)
pickle.dump(cal_sens, open('cal','wb'))

