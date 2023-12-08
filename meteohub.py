#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2018/08/03
########################################################################

import RPi.GPIO as GPIO

from dependencies.lcd.PCF8574 import PCF8574_GPIO
from dependencies.lcd.Adafruit_LCD1602 import Adafruit_CharLCD
import dependencies.hygrotherm.Freenove_DHT as DHT

from time import sleep

DHTPin = 11                                 # define the pin of DHT11

PERCENTAGE_CHAR = chr(37)
DEGREE_CELSIUS_CHAR = chr(223)

def loop():
    mcp.output(3,1)                         # turn on LCD backlight
    lcd.begin(16,2)                         # set number of LCD lines and columns
    dht = DHT.DHT(DHTPin)                   # create a DHT class object

    while(True):

        for i in range(0,15):
            chk = dht.readDHT11()           # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            if (chk == dht.DHTLIB_OK):      # read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
                break

        formatted_temp = "Tmp: %.1f%sC %s" % (dht.temperature, DEGREE_CELSIUS_CHAR, get_level_message(dht.temperature, temperature_levels))
        formatted_humidity = "Hum: %d%s %s" % (dht.humidity, PERCENTAGE_CHAR, get_level_message(dht.humidity, humidity_levels))

        lcd.setCursor(0,0)                  # set cursor position
        lcd.message(formatted_temp + '\n')  # display temperature
        lcd.message(formatted_humidity)     # display humidity

        sleep(0.2)

# Define the temperature ranges and their short descriptions
temperature_levels = {
    (-50, 0):  ":X",
    (0, 10):   ":*",
    (10, 20):  ":|",
    (20, 30):  ":)",
    (30, 40):  ":/",
    (40, 50):  ":S",
    (50, 100): ":O",
}

# Define the humidity ranges and their descriptions
humidity_levels = {
    (0.0, 30.0):   "Dry  :[",
    (30.0, 50.0):  "Good :)",
    (50.0, 60.0):  "Nice :D",
    (60.0, 70.0):  "Fair :]",
    (70.0, 80.0):  "Ick  :/",
    (80.0, 90.0):  "Bad  :(",
    (90.0, 100.0): "No!  :O",
}

def get_level_message(level, level_messages):
    """Return the comfort level based on the levels percentage."""
    for range_start, range_end in level_messages:
        if range_start <= level < range_end:
            return level_messages[(range_start, range_end)]
    return "??"                             # In case the humidity is out of the defined ranges


def destroy():
    lcd.clear()

PCF8574_address = 0x27                      # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F                     # I2C address of the PCF8574A chip.

# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('LCD I2C Address Error!')
        exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Meteohub is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        destroy()
        exit()

