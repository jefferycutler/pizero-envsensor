import adafruit_scd30
import board
import busio
from datetime import datetime
from RPLCD.i2c import CharLCD
#from sht_sensor import Sht
from time import sleep

##### Set our pins for the sht sensor
#sck_pin=21
#data_pin=17
lcd_rows=4
lcd_cols=20

##### setup our LCD connection
lcd=CharLCD(i2c_expander='PCF8574', address=0x27, port=1,cols=lcd_cols,
            rows=lcd_rows, dotsize=8,charmap='A02',auto_linebreaks=True,
            backlight_enabled=True)
lcd.clear()

##### Setup our Adafruit sensor 
#sht=Sht(sck_pin,data_pin)
i2c=busio.I2C(board.SCL, board.SDA, frequency=50000)
scd=adafruit_scd30.SCD30(i2c)

##### start a loop that gets readings and displays every second
# The outer loop is continous but the inner loop ensures
# the screen is cleared and refreshed every 10 minutes
while True:
	for x in range(20):
		now = datetime.now()
		if scd.data_available:
			co2=round(scd.CO2)
			temp=round(scd.temperature)
			humd=round(scd.relative_humidity)
		#temp=round(sht.read_t())
		#humd=round(sht.read_rh())
		lcd.cursor_pos=(0,0)
		lcd.write_string(now.strftime("%a %b %d %I:%M %p\r\n"))
		####  depending on number of rows print temp and humidity
		if lcd_rows>=4:
			lcd.cursor_pos=(1,0)
			lcd.write_string(f"Temperature:{temp}C\r\n")
			lcd.cursor_pos=(2,0)
			lcd.write_string(f"Humidity:{humd}\r\n")
			lcd.cursor_pos=(3,0)
			lcd.write_string(f"CO2:{co2} PPM\r\n")
		elif lcd_rows==2:
			lcd.cursor_pos=(1,0)
			lcd.write_string(f"T:{temp}C H:{humd}%")
		sleep(30)
	# now refresh screen
	lcd.clear()




