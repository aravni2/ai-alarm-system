import LCD1602
import time

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
