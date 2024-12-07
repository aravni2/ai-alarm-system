# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.12
#
# Description:
    # This file creates the pin connections needed to use the keypad, although there are 16 buttons with the need for 32 i/o pins
    # by using row/column matrix it only requires 4 pins for input (rows) and 4 pins for output (columns).complex
    # the buttons on the keypad represent open connections. once a button is pushed  the connection between voltage inn (row)
    # and voltage output/read (column) is completed, because it is connected, voltage must be sent individually between each row and
    # then each column would be checked for high (1) output.
        
    # In addition the circuits need to be locked if a button is pushed down indefinitely so that only one input is read and not 
    # continual values. once the button is released the circuit can then take the same or a new value.

    # currently this is checked for the exact button but another version could be just looking if a button was pressed in the loop
    # and assigning a locked value so the next loop (if still pressed) would not send value


#   dht11 Temperature sensor with LCD1602 module are used to collect temperature and humidity settings and send them to 
#   the LCD display. This will later be used to detect fire/flood


import RPi.GPIO as GPIO
import time

# set pin numbers
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

# create a button lock to avoid held down buttons giving multiple inputs
# btn_lock = False
# last_button = None

# set up keypad inputs
# keypad = [
#     [1,2,3,'A'],
#     [4,5,6,'B'],
#     [7,8,9,'C'],
#     ['*',0,'#','D']
#     ]


GPIO.setmode(GPIO.BOARD)
# set RPI pins for output/input
GPIO.setup(r0_out_pin,GPIO.OUT)
GPIO.setup(r1_out_pin,GPIO.OUT)
GPIO.setup(r2_out_pin,GPIO.OUT)
GPIO.setup(r3_out_pin,GPIO.OUT)

GPIO.setup(c0_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c1_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c2_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(c3_in_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)


class Keypad():
    def __init__(self):
        self.row_pins=[11,13,15,29]

        # r0_out_pin = 11
        # r1_out_pin = 13
        # r2_out_pin = 15
        # r3_out_pin = 29

        self.column_pins = [31,33,35,37]
        
        # c0_in_pin = 31
        # c1_in_pin = 33
        # c2_in_pin = 35
        # c3_in_pin = 37

        self.keypad = [
            ['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['*','0','#','D']
            ]
    
        self.val = 0
        self.last_button = None
        self.key = None
        self._pwd = '1234'
        self.entry = ''
        self.is_pressed = False
        self.btns_locked = False
        self.change_pass = False

        self.status = ''
                                                       

    def check_kp_press(self):
        # iterate through rows giving each row power and checking if circuit is complete in columns
        for row_idx in range(4):
            # turn current rows output on
            GPIO.output(self.row_pins[row_idx],GPIO.HIGH)

            # iterate through columns checking for completed circuit
            for col_idx in range(4): 
                self.val = GPIO.input(self.column_pins[col_idx])
                
                # get key press value and if it's been held down 
                self.check_keypad(row_idx,col_idx)

            GPIO.output(self.row_pins[row_idx],GPIO.LOW)


    def check_keypad(self,row_idx,col_idx):
        # check if button is pressed, get value of key
        if self.val ==1:
            # check to see if button has been held down
            if self.last_button != [row_idx,col_idx]:
                # assign key pad value to key variable
                self.key = self.keypad[row_idx][col_idx]
                # self.entry = self.entry + self.key
                self.validate_entry()
                
                print('key pressed:', self.key)
                # print('new cycle')
                self.last_button=[row_idx,col_idx]

        # check to see if button that was previously pressed in last loop is now unpressed. this can also be done with
        # locking true/false values and if a button is pressed in current loop
        if self.val ==0 and [row_idx,col_idx] == self.last_button:
            self.last_button= None
    
    def validate_entry(self):
        """Check each entry to see if it is a command (D,A,C) or simply another number to add to entry"""

        if self.key in  ('D','A','C'):
            print(self.entry)
            self.check_pass()
            # clear entry out
            self.entry = ''
        else:    
            self.entry = self.entry + self.key

        if len(self.entry)>8:
            print('Entry too Long!!')

        # print(self.entry)
    def check_pass(self):
        if self.entry == self._pwd and self.key == 'D':
            self.status = 'DISARMING'
            print('DISARMED')
        elif self.entry == self._pwd and self.key =='A':
            self.status = 'ARMING'
            print('ARMED')
        elif self.entry ==self._pwd and self.key =='C':
            self.change_pass = True
            print('Please enter new password followed by "C" ')
        elif self.change_pass== True and len(self.entry)>3 and self.key == 'C':
            self._pwd = self.entry
            self.change_pass = False
        else:
            print('Incorrect Entry')





if __name__ == '__main__':

    try:
        kp = Keypad()
        while True:
            kp.check_kp_press()
            # for row_idx in range(4):
            #     GPIO.output(row_pins[row_idx],GPIO.HIGH)

            #     for col_idx in range(4): 
            #         val = GPIO.input(column_pins[col_idx])
            #         last_button = check_keypad(val,row_idx,col_idx,last_button)
                    # if val ==1:
                    #     if last_button == keypad[row_idx][col_idx]:
                    #         pass
                    #         # print('button held down')
                    #     else: 
                    #         key = keypad[row_idx][col_idx]
                    #         print('key pressed:', key)
                    #         # print('new cycle')
                    #         last_button=key
                    # if val ==0 and keypad[row_idx][col_idx] == last_button:
                    #     last_button= None
                # GPIO.output(row_pins[row_idx],GPIO.LOW)
            time.sleep(.02)
            
        


    except KeyboardInterrupt:
        time.sleep(.2)
        GPIO.cleanup()
        print('GPIO cleaned up')



