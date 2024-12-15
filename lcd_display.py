import LCD1602
import time
# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
    # SEE LCD1602.py module This File utilizes an LCD1602 library we found on the "TopTechBoy" youtube channel. it appears he received this library from someone else, but
    # this is only a test of the system

LCD1602.init(0x27,1)


def main():
    while True:
        LCD1602.write(0,0,"Hello World")
        LCD1602.write(0,1, 'WELCOME!!!!')



if __name__ == '__main__':
  
    try:
        main()
    except KeyboardInterrupt:
        time.sleep(.5)
        LCD1602.clear()
        print('LCD cleared')
