#############################################################################################
#  envsensor.py
#   Python script to get temperpature, humidity, and co2 levels from the
#    adafruit SCD30 sensor, display to LCD screen 
#############################################################################################
import adafruit_scd30
import board
import busio
import configparser
from datetime import datetime
import json
import logging
from logging.handlers import SysLogHandler
import os
import socket
from sht_sensor import Sht
from RPLCD.i2c import CharLCD
from time import sleep

########## Config options here ###############################
sensor="office"  # name for this sensor in database later
sensor_freq=60   # delay between measurements in seconds
syslogip='192.168.40.100'  # syslog host receiving msg
syslogport=514             # syslog destination port
sck_pin=21            # SHT temp sensor SCK pin used on GPIO
data_pin=17           # SHT Temp sensor data pin used on GPIO 
lcd_cols=20           # How many columns in the LCD display
lcd_rows=4            # how many rows in the LCD display

########## Should not need to modify below this line #########

### function to fix the time zone string, needs a colon at pos 23 for BigQueyr
def clean_tz(str):
    return str[:22] + ":" + str[22:]

##### get this devices configuration
config=configparser.ConfigParser()
config.read(os.getcwd() + '/config.ini')

## setup our rsyslog reporting
hostname = socket.gethostname()
logger = logging.getLogger('envsensor')
logger.setLevel(logging.INFO)
syslog = SysLogHandler(address=(syslogip, syslogport))
formatter = logging.Formatter('%(asctime)s %(name)s: %(message)s', '%b %e %H:%M:%S')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

### Setup sht sensor
sht=Sht(sck_pin,data_pin)

##### setup our LCD connection
lcd=CharLCD(i2c_expander='PCF8574', address=0x27, port=1,cols=lcd_cols,
            rows=lcd_rows, dotsize=8,charmap='A02',auto_linebreaks=True,
            backlight_enabled=True)
lcd.clear()

##### Setup our Adafruit sensor
i2c=busio.I2C(board.SCL, board.SDA, frequency=50000)
scd=adafruit_scd30.SCD30(i2c)

# set some defaults in case we can't read values, prevents null errors
co2=0
temp=-99
humd=-99

##### start a loop that gets readings and displays every second
# The outer loop is continous but the inner loop ensures
# the screen is cleared and refreshed every 10 minutes
while True:
        for x in range(10):
                now = datetime.now().astimezone()
                # read the sensor data
                co2=round(scd.CO2)
                temp=round(sht.read_t())  # scd30 was round(scd.temperature)
                humd=round(sht.read_rh())  #scd30 was round(scd.relative_humidity)
                # Build the rsyslog message payload
                payload={"sensor":sensor,
                        "sensor_timestamp":clean_tz(now.strftime("%Y-%m-%dT%H:%M:%S%z")),
                        "temperature":temp,
                        "humidity":humd,
                        "co2":co2 }
                logger.info(json.dumps(payload))
                lcd.cursor_pos=(0,0)
                lcd.write_string(now.strftime("%a %b %d %I:%M %p\r\n"))
                ####  depending on number of rows print temp and humidity
                if lcd_rows>=4:
                        lcd.cursor_pos=(1,0)
                        lcd.write_string(f"Temperature:{temp}C  \r\n")
                        lcd.cursor_pos=(2,0)
                        lcd.write_string(f"Humidity:{humd}  \r\n")
                        lcd.cursor_pos=(3,0)
                        lcd.write_string(f"CO2:{co2} PPM  \r\n")
                elif lcd_rows==2:
                        lcd.cursor_pos=(1,0)
                        lcd.write_string(f"T:{temp}C H:{humd}% CO2:{co2} PPM  ")
                sleep(sensor_freq) 
        # now refresh screen
        lcd.clear()
