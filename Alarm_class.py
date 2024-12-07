# Ghosananda Wijaya and Anthony Ravnic 
# CS437
# 2024.10.08
# 
# Description:
    # Creates a class for handling the Arm/Disarm functions of the alarm, along with the sounds accompanied with it
    # Uses pygames volume/sound mixer to run sounds on a channel that can be started,stopped, and re-loaded. The alarm sirens
    #  consist of a soft (arming) alarm and a hard alarm when a time period elapses without disarming the system

import pygame
import time


class Alarm():
    def __init__(self, arm_cycle = 5, soft_cycle = 5) -> None:
        # Flags for determining whether soft or hard alarm is playing and cylcing between them
        self.soft_alarm = 0
        self.hard_alarm = 0

        # flag denoting if system is armed
        self.is_armed = 0
        # timing to denote shift from soft alarm to hard alarm
        self.start = time.time()
        self.siren_duration =0

        # cycling time for transition from arming to armed
        self.arm_cycle = arm_cycle

        # cycling time to transition from soft alarm to hard alarm when sirening
        self.soft_cycle = soft_cycle

        # pygame sound mixer set up and tracks
        self.channel = pygame.mixer.Channel(0)
        self.s_alarm = pygame.mixer.Sound('soft_alarm.wav')
        self.h_alarm = pygame.mixer.Sound('hard_alarm.mp3')

    def arm(self):
        """function to trigger arming of system along with soft_alarm duration. 
        arm_cycle is inputted to denote how long the system takes from arming to armed.
        Time.sleep is used as we want to pause all functions in this transitory state

        Arm cycle also determines how long the soft alarm plays for
        Args:
            arm_cycle: duration of arming in seconds
        """
        if self.is_armed ==0:
            self.channel.play(self.s_alarm,-1)
            time.sleep(self.arm_cycle)
            self.channel.stop()
            self.is_armed = 1
            self.start = time.time()

    def disarm(self):
        """Disarm function to reset internal soft/hard alarm transitions and amring flags
        """
        self.is_armed = 0
        self.soft_alarm=0
        self.hard_alarm = 0
        self.start = 0
        self.siren_duration = 0
        self.channel.stop()

    def siren(self):
        """Creates siren and manages internal flags to determine which alarm (soft or hard) to play and when to transition
        between soft and hard alarms.

        Args:
            soft_cycle (_type_): determines how long the soft alarm plays before cylcing to hard alarm
        """
        # check if soft alarm or hard alarm is playing, if not start timer and start soft alarm
        if self.soft_alarm==0 and self.hard_alarm==0:
            self.start = time.time()
            self.channel.play(self.s_alarm,-1)
            # flip soft alarm flag to true
            self.soft_alarm=1
        # conditional to flip to hard alarm when soft alarm is playing, hard alarm is not and the soft cycle transition time
        # has been met
        elif self.soft_alarm==1 and self.hard_alarm==0 and (self.siren_duration)>self.soft_cycle:
            self.channel.stop()
            self.channel.play(self.h_alarm,-1)
            self.hard_alarm=1
        # calculate duration alarm has played
        self.siren_duration = time.time()- self.start
        


if __name__ == '__main__':
    # initiate pygame
    pygame.init()

    
    arm_cycle = 10
    soft_cycle = 5
    passcode= 1234
    alarm = Alarm()
    # test arm disarm cycles
    while True:
        # alarm.is_armed=1
        alarm.arm()
        print(alarm.is_armed)
        alarm.siren()
        if (alarm.siren_duration>15):
            alarm.disarm()
        print('arm to disarm time:',alarm.soft_alarm,alarm.hard_alarm,alarm.siren_duration)


        
        
    
        


    


