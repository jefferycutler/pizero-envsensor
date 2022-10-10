####################################################################################
# envsensor-nodisplay.py
#    Gather environmental data and report back to central relay
#    this version does not have a display (headless)
####################################################################################
import adafruit_scd30
import board
import busio
from datetime import datetime
import json
import logging
from logging.handlers import SysLogHandler
import socket
from sht_sensor import Sht
from time import sleep

########## Config options here ###############################
sensor="backyard" # name for this sensor in database later
sensor_freq=60   # delay between measurements in seconds
syslogip='192.168.40.100' # syslog host receiving msg
syslogport=514            # syslog destination port
sck_pin=21             # SHT temp sensor SCK pin used on GPIO
data_pin=17            # SHT Temp sensor data pin used on GPIO

########## Should not need to modify below this line #########

### function to fix the time zone string, needs a colon at pos 23 for BQ
def clean_tz(str):
    return str[:22] + ":" + str[22:]

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

### Setup SCD30
i2c=busio.I2C(board.SCL, board.SDA, frequency=50000)
scd=adafruit_scd30.SCD30(i2c)

while True:
        now = datetime.now().astimezone()
        ### Go get values
        sht_temp=round(sht.read_t())
        sht_humid=round(sht.read_rh())
        co2=round(scd.CO2)
        ### report results
        payload={"sensor":sensor,
                "sensor_timestamp":clean_tz(now.strftime("%Y-%m-%dT%H:%M:%S%z")),
                "temperature":sht_temp,
                "humidity":sht_humid,
                "co2":co2 }
        logger.info(json.dumps(payload))
        sleep(sensor_freq)
