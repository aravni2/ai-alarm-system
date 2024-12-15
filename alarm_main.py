import RPi.GPIO as GPIO   #lgpiod, a shell for rpi.gpio
import pygame  #pygame for audio channel mixer
import time
import dht11  #Temp sensor
import cv2
import LCD1602  #LCD Screen
import time
from datetime import datetime
from keypad import Keypad
from az_data_lake_class import data_lake
from az_key_vault import get_kv_secret  #used to securely retrieve secrets
from Alarm_class import Alarm
from facial_rec_class import Video
# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
    # This is the main alarm function that incorporates all the modules into a loop. the main loop:
    # 1. initializes all the modules and sensors, including a pull push of known faces to the cloud 
    # 2. checks for fire first and foremost, but remains unarmed
    # 3. temperature and humidity are reported via the keypad along with alarm status
    # 4. arming the system via keypad ("1234" + "A") then triggers a soft alarm (to leave house). 
    # 5. Once armed a series of triggers check for motion and initializes the camera (though not recording) when in armed state
    # 6. if motion is detected, the Alarm() class triggers the siren and a soft alarm starts (5 seconds for demo speed) followed by a hard alarm siren 
    # 7. once soft alarm is triggered the camera starts taking pictures on an interval (default 3 seconds) starting with one picture taken immediately.
    # 8. pictures are then uploaded into the cloud and stored for user to check in browser or app
    # 9. it also checks every other frame (for processing speed up) to see if a person in frame matches to the "known faces" 
    #       if so, system is disarmed and camera is turned off. if not, the siren continues to play and pictures are uploaded to cloud
    # 10. disarming can also be done via the keypad as well, but simply typing in 1234 +"D"
    #ADDITIONAL FEATURES:
    # the system also allows for changing password by typing 1234 + "C" then "<newpass>"+"C"
    #and additional buzzer was set up to sound off whenever motion was detected, this is an active buzzer and is not tonally changed


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
    """Helper fucntion to report temperature/humidity to LCD screen

    
    """
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
    """helper function to detect motion and return it to a sentinal variable in loop"""
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
    # set up azure cloud data lake storage for captured images
    adl_account = get_kv_secret('adl-alarm-name')
    data_L = data_lake(adl_account=adl_account,lcl_file_path = 'captures')

    # sync known faces with cloud account
    data_L.pull_push_known_faces()
    
    # initiate pygame for channels/mixer
    pygame.init()

    # Initialize relevant classes
    alarm = Alarm()
    kp = Keypad()
    vid = Video()
    vid.load_faces()




    # add sentinal variable for motion detection/alarm siren trip
    motion = 0

    # add time delta to keep track of when to take pictures. Delta starts off large so once alarm is triggered it auto takes pic
    delta = 0
    previous_time = 0

    try:
        time.sleep(.2)
        while True:

            current_time = time.time()
            delta += current_time - previous_time
            previous_time = current_time 

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
                vid.initiate_capture()
            elif kp.status == 'DISARMING':
                alarm.disarm()
                kp.status = ''
                motion = 0
                vid.video_capture.release()
                cv2.destroyAllWindows()
                vid.clean_up_capture()
            # Armed State checks
            motion = max(motion, detect_motion())
            if alarm.is_armed ==1  and motion==1:
                alarm.siren()
                matches, frame = vid.check_faces()
                LCD1602.write(0,0,f'INTRUDER ALERT!!')



                # face matches to known faces (disarm and clear variables)
                if matches:
                    alarm.disarm()
                    kp.status = ''
                    
                    motion=0
                    
                    # clean out video capture and remove any windows that could be storing older frames
                    vid.video_capture.release()
                    cv2.destroyAllWindows()
                    vid.clean_up_capture()

                # start taking and sending pictures to cloud every 3 seconds 
                elif delta>=3:
                    print('taking photo')
                    im_name = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}_.png'
                    vid.write_images(im_name)
                    data_L.send_files(im_name)
                    delta = 0

            # write statuses to LCD screen, spaces in strings ensure all characters are overwritten
            elif alarm.is_armed:

                LCD1602.write(0,0,f'Armed           ')
            elif temp >110:
                LCD1602.write(0,0,f'FIRE Detected!  ')
            else:
                LCD1602.write(0,0,f'Disarmed        ')


            

    except KeyboardInterrupt:
        time.sleep(.2)
        LCD1602.clear()
        time.sleep(.2)
        GPIO.cleanup()
        print('GPIO cleaned up')

        
            

