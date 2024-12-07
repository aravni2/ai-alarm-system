import gpiod
from RPi import GPIO
from time import sleep

dt = .1
b1 = 40
b2 = 38
b3 = 33 
b1_state = 1
b1_state_old = 1

b2_state= 1
b2_state_old = 1

LEDPin = 37

DC = 99 #duty cycle

GPIO.setmode(GPIO.BOARD)
GPIO.setup(b1,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(b2,GPIO.IN,pull_up_down=GPIO.PUD_UP )

GPIO.setup(LEDPin,GPIO.OUT)
GPIO.setup(b3, GPIO.OUT)


myPWM = GPIO.PWM(LEDPin,100)

myPWM.start(DC)


try:
    while True:
        b1_state = GPIO.input(b1)
        b2_state = GPIO.input(b2)
        if b1_state_old==0 and b1_state == 1:
            
            DC -=10
            print('dim event')
        if b2_state_old==0 and b2_state==1:
            DC+=10
            print('brighten event')
        if DC >99:
            DC=99
        if DC <0:
            DC = 0
        if DC== 99:
            GPIO.output(b3,GPIO.HIGH)
        else:
            GPIO.output(b3,GPIO.LOW)
            print('max')
        myPWM.ChangeDutyCycle(DC)
        b1_state_old = b1_state
        b2_state_old = b2_state
        sleep(dt)



except KeyboardInterrupt:
    myPWM.stop()
    GPIO.cleanup()
    print('gpio good to go')