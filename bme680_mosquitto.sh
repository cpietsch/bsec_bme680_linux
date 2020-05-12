#!/bin/bash
sleep 60
cd /home/pi/bsec_bme680_linux
/usr/bin/screen -d -m bash -c "/home/pi/bsec_bme680_linux/bsec_bme680 | mosquitto_pub -h 192.168.10.37 -p 1883 -t home/pizero/bme680 -l"
