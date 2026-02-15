#!/usr/bin/env python3
#added some features, buzzer alarm on power down, driven by gpio 27 to npn

import os
import sys
import time

import RPi.GPIO as GPIO

SHUTDOWN_BTN = 11  # GPIO_GEN0 (BCM #17)
SHUTDOWN_LED = 12  # GPIO_GEN1 (BCM #18)
POWER_CHECK = 15 # (BCM #22)
POWER_ALARM_BUZZER = 13 (BCM #27)
T_CHECK = 1000  # in milliseconds
T_HOLD = 5000  # in milliseconds
T_BLINK = 100  # in milliseconds
BLINK_COUNT = 5


def main() -> int:
    print('Raspi-safe-shutdown started. Waiting for the user to press the',
          'shutdown button')

    GPIO.setmode(GPIO.BOARD)  # Physical/board pin-numbering scheme

    GPIO.setup(SHUTDOWN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SHUTDOWN_LED, GPIO.OUT)
    GPIO.setup(POWER_CHECK, GPIO.IN)
    
    GPIO.output(SHUTDOWN_LED, GPIO.LOW)
    GPIO.setup(POWER_ALARM_BUZZER, GPIO.OUT)
    GPIO.output(POWER_ALARM_BUZZER, GPIO.LOW)
    
    
    

    while True:
        if GPIO.input(SHUTDOWN_BTN):
            print('Button pressed. Waiting', T_HOLD, 'milliseconds...')

            GPIO.output(SHUTDOWN_LED, GPIO.HIGH)
            time.sleep(T_HOLD / 1000.0)
            GPIO.output(SHUTDOWN_LED, GPIO.LOW)

            if GPIO.input(SHUTDOWN_BTN):
                print('The button is still pressed. Shutting down')

                for _ in range(BLINK_COUNT):
                    GPIO.output(SHUTDOWN_LED, GPIO.LOW)
                    time.sleep(T_BLINK / 1000.0)
                    GPIO.output(SHUTDOWN_LED, GPIO.HIGH)
                    time.sleep(T_BLINK / 1000.0)

                GPIO.cleanup()
                os.execvp('poweroff', ['poweroff'])
            else:
                print('Button released. Waiting again for the user to press',
                      'the shutdown button')
       
        if GPIO.input(POWER_CHECK)==0:
            print('Power only from backup battery, shutting down:')
            for _ in range(BLINK_COUNT):
                    GPIO.output(POWER_ALARM_BUZZER, GPIO.LOW)
                    time.sleep(T_BLINK / 1000.0)
                    GPIO.output(POWER_ALARM_BUZZER, GPIO.HIGH)
                    time.sleep(T_BLINK / 1000.0)
            #os.execvp('poweroff', ['poweroff'])
        
        
        
        time.sleep(T_CHECK / 1000.0)


if __name__ == '__main__':
    sys.exit(main())
