import subprocess
import json
import time
from influxdb import InfluxDBClient
import datetime
import math

client = InfluxDBClient(host='192.168.0.205', port=8086)
client.switch_database('logs1')

p = subprocess.Popen('/home/pi/bsec_bme680_linux-mod/bsec_bme680', stdout=subprocess.PIPE, stderr = None, shell=True)

for line in iter(p.stdout.readline, ''):
    sensor_clean = {}
    sensor = json.loads(line)
    for k, v in sensor.items():
        try:
                sensor_clean[k] = float(v)
        except:
                pass
    #print(sensor['Temperature'])
    #sensor['Temperature'] = float(sensor["Temperature"])

    #print(sensor_clean)
    point = { "measurement": "sensor4", "fields": sensor_clean }
    client.write_points([point])


p.stdout.flush()
p.stdout.close()

print ("Done")
