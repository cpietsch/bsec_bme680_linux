#!/bin/bash
/opt/bsec_bme680/bsec_bme680 | tee -a /var/log/bsec_bme680.log | mosquitto_pub -h 192.168.10.37 -p 1883 -t home/pizero/bme680 -l
