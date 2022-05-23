#!/bin/bash
###################################################################
# envsensor.sh
#   Script to run on a pi zero with LCD attached and Adafruit 
#   SCD-30 DNIR CO2, temp and humidity sensor
###################################################################

# first activate the python environment
source /opt/envsense/pyenv/bin/activate

# now run the python envsensor script
python /opt/envsense/envsensor.py

#
