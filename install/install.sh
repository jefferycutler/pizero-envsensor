#!/bin/bash
##############################################################
# install script for Pi Zero Environmental sensor node
#
##############################################################

read -p "Do you have an I2C LCD Display?" yn
case $yn in
	[Yy]* ) echo -e "Installing I2C display refresh service";;
	* ) echo -e "Skipping display"
esac


