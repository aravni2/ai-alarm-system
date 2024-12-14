import RPi.GPIO as GPIO
import time
# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
# potentiometer on the right controls the senstitivity , and the potentiometer on the left controls the timeout. 
# counter clockwise is lowest setting for both
#  timeout - fully anticlockwise timesout for 2.5 seconds, fully clockwise times out for 250seconds. best to leave this low while 
    # tuning sensitivity
# Sensitivity - can tune between 3 and 7 meters


pir_pin = 36
mot_siren = 1
GPIO.setmode(GPIO.BOARD)

if mot_siren ==1:
    sir_pin = 18
    GPIO.setup(sir_pin,GPIO.OUT)
GPIO.setup(pir_pin, GPIO.IN)




def detect_motion():
    while True:
        motion = GPIO.input(pir_pin)
        print(motion)

        if motion ==1 and mot_siren==1:
            GPIO.output(sir_pin,GPIO.HIGH)
        if motion==0:
            GPIO.output(sir_pin,GPIO.LOW)
        time.sleep(.1)


if __name__=='__main__':


    print('warming up pir sensor')
    time.sleep(10)


    try: 
        detect_motion()


    except KeyboardInterrupt:
        GPIO.cleanup()
        print('GPIO Cleaned up')



