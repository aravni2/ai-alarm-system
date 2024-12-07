import RPi.GPIO as GPIO
import ADC0834
import time
 
GPIO.setmode(GPIO.BCM)
ADC0834.setup()
try:
    while True:
        analogVal=ADC0834.getResult(0)
        print(analogVal)
        # voltage_val= (5*analogVal)/1024
        # cels_temp_val = (voltage_val-.45)*100
        
        # print(voltage_val,cels_temp_val)
        # far_temp = (cels_temp_val*(9/5))+32
        # print("farenheit temp:",far_temp)
        time.sleep(.2)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO Good to Go')