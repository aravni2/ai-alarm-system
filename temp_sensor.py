# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.02
# 
# Description:
#   dht11 Temperature sensor with LCD1602 module are used to collect temperature and humidity settings and send them to 
#   the LCD display. This will later be used to detect fire/flood





import RPi.GPIO as GPIO
import time
import dht11
import LCD1602

temp_pin =16
LCD1602.init(0x27,1)
GPIO.setmode(GPIO.BOARD)
temp_sensor = dht11.DHT11(pin = temp_pin)





def main():

    while True:
        TH_result = temp_sensor.read()
        if TH_result.is_valid():
            temp_cels = TH_result.temperature
            temp_far = (temp_cels*(9/5))+32
            print('Temperature:', temp_far, "Humidity %:", TH_result.humidity)
            # print(TH_result)
            
            LCD1602.write(0,0, f'Temp: {int(temp_far)}')
            LCD1602.write(0,1,f'Humidity: {TH_result.humidity}')
        time.sleep(.5)
        # LCD1602.clear()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        LCD1602.clear()
        print('GPIO cleaned up')
