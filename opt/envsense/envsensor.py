import adafruit_scd30
import board
import busio
import configparser
from datetime import datetime
import json
from kafka import KafkaProducer
import os
from RPLCD.i2c import CharLCD
from time import sleep

##### get this devices configuration
config=configparser.ConfigParser()
config.read(os.getcwd() + '/config.ini')
lcd_cols=config['lcd'].getint('cols')
lcd_rows=config['lcd'].getint('rows')
#brokers=config['kafka']['brokers']
#sensor=

#print(brokers)
#raise SystemExit(0)

##### setup our LCD connection
lcd=CharLCD(i2c_expander='PCF8574', address=0x27, port=1,cols=lcd_cols,
            rows=lcd_rows, dotsize=8,charmap='A02',auto_linebreaks=True,
            backlight_enabled=True)
lcd.clear()

##### Setup our Adafruit sensor 
i2c=busio.I2C(board.SCL, board.SDA, frequency=50000)
scd=adafruit_scd30.SCD30(i2c)

##### Setup our Kafka producer
#broker_list='k01:9092,k02:9092,k03:9092'
producer=KafkaProducer(bootstrap_servers=config['kafka']['brokers'])

##### start a loop that gets readings and displays every second
# The outer loop is continous but the inner loop ensures
# the screen is cleared and refreshed every 10 minutes
while True:
	for x in range(10):
		now = datetime.now().astimezone()
		# read the sensor data
		if scd.data_available:
			co2=round(scd.CO2)
			temp=round(scd.temperature)
			humd=round(scd.relative_humidity)
			# send this data to kafka
			payload={"sensor":config['kafka']['sensor'],
				"sensor_timestamp":now.strftime("%m-%d-%Y %H:%M:%S %z"),
				"temperature":temp,
				"humidity":humd,
				"co2":co2 }
			producer.send('remote-test',bytes(json.dumps(payload),'utf-8'))
			producer.flush()
			
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
		sleep(60)
	# now refresh screen
	lcd.clear()


