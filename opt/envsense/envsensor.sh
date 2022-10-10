#!/bin/bash
###################################################################
# envsensor.sh
#   Script to run on a pi zero with LCD attached and Adafruit 
#   SCD-30 DNIR CO2, temp and humidity sensor
###################################################################

USE_DISPLAY=Y

# first activate the python environment
source /opt/envsense/pyenv/bin/activate

# run python script depending on display option
if [ $USE_DISPLAY = "Y" ]
then
        echo "INFO: Running with LCD display"
        python /opt/envsense/envsensor-display.py
else
        echo "INFO: Running in headless mode"
        python /opt/envsense/envsensor-nodisplay.py
fi
