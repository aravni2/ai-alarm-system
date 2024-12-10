import RPi.GPIO as GPIO   #lgpiod, a shell for rpi.gpio
import pygame  #pygame for audio channel mixer
import time
import dht11  #Temp sensor
import cv2
import LCD1602  #LCD Screen
from keypad import Keypad

from Alarm_class import Alarm
from facial_rec_class import Video



GPIO.setmode(GPIO.BOARD)

# ///////////PIN SETUPS////////////////
# Infrared motion sensor
pir_pin = 36

# small active buzzer pin
sir_pin = 18

# Temp sensor setup, temp sensor acts as both pin setup but uses class to read as well
temp_pin =16
temp_sensor = dht11.DHT11(pin = temp_pin)

# setup LCD i2C connection, uses serial clock and data pins 3 and 5
LCD1602.init(0x27,1)


# Keypad Pins
# row_pins=[11,13,15,29]
r0_out_pin = 11
r1_out_pin = 13
r2_out_pin = 15
r3_out_pin = 29
# column_pins = [31,33,35,37]
c0_in_pin = 31
c1_in_pin = 33
c2_in_pin = 35
c3_in_pin = 37
# keypad layout
# keypad = [
#     [1,2,3,'A'],
#     [4,5,6,'B'],
#     [7,8,9,'C'],
#     ['*',0,'#','D']
#     ]




GPIO.setup(sir_pin,GPIO.OUT) #siren setup (can remove)
GPIO.setup(pir_pin, GPIO.IN) #pir pin setup

# KEYPAD, set RPI pins for output
GPIO.setup(r0_out_pin,GPIO.OUT)
GPIO.setup(r1_out_pin,GPIO.OUT)
GPIO.setup(r2_out_pin,GPIO.OUT)
GPIO.setup(r3_out_pin,GPIO.OUT)
# KEYPAD, RPI pins for reading input (closed circuit if button pushed)
GPIO.setup(c0_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c1_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c2_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c3_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


def report_temp():
    TH_result = temp_sensor.read()
    if TH_result.is_valid():
        temp_cels = TH_result.temperature
        temp_far = (temp_cels*(9/5))+32
        # print('Temperature:', temp_far, "Humidity %:", TH_result.humidity)
        # print(TH_result)
        LCD1602.write(0,1, f'Temp/Hum: {int(temp_far)}/{int(TH_result.humidity)}%')
        # LCD1602.write(0,0, f'Temp: {int(temp_far)}')
        # LCD1602.write(0,1,f'Hum: {int(TH_result.humidity)}%')
        return temp_far, TH_result.humidity
    else:
        return -1,-1
    
def detect_motion():
    motion = GPIO.input(pir_pin)
    

    if motion ==1:
        print('Motion Detected!!')
        # still send motion beeps if armed/disarmed
        GPIO.output(sir_pin,GPIO.HIGH)
        return 1
    if motion==0:
        GPIO.output(sir_pin,GPIO.LOW)
        return 0
    



if __name__ == '__main__':
    # initiate pygame for channels/mixer
    pygame.init()

    alarm = Alarm()
    kp = Keypad()
    vid = Video()
    vid.load_faces()
    motion = 0

    try:
        time.sleep(.2)
        while True:

            # check temperatures for fire outside of arm/disarm cycle
            temp,hum =report_temp()
            if temp > 110:
                alarm.siren()

            # check keypad for key entries or commands
            kp.check_kp_press()

            # check if keypad commands have been entered to arm disarm system
            if kp.status == 'ARMING':
                alarm.arm()
                motion = 0
                kp.status = ''
            elif kp.status == 'DISARMING':
                alarm.disarm()
                kp.status = ''
                motion = 0
                vid.video_capture.release()
                cv2.destroyAllWindows()
            # Armed State checks
            motion = max(motion, detect_motion())
            if alarm.is_armed ==1  and motion==1:
                alarm.siren()
                matches, frame = vid.check_faces()
                LCD1602.write(0,0,f'INTRUDER ALERT!!!')
            
            elif alarm.is_armed:

                LCD1602.write(0,0,f'Armed')
            elif temp >110:
                LCD1602.write(0,0,f'FIRE Detected!')
            else:
                LCD1602.write(0,0,f'Disarmed')


            

    except KeyboardInterrupt:
        time.sleep(.2)
        LCD1602.clear()
        GPIO.cleanup()
        print('GPIO cleaned up')

        
            

