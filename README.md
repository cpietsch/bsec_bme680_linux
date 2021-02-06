# bsec_bme680_linux

Read the BME680 sensor with the BSEC library on Linux (e.g. Raspberry Pi)

This repo adds a read.py script to parse the JSON Values of the sensor and sends it directly to a InfluxDB server.

## Intro

Working example of fully using the
[BME680 sensor](https://www.bosch-sensortec.com/en/bst/products/all_products/bme680)
on Linux (e.g. Raspberry Pi) with the precompiled
[BSEC library](https://www.bosch-sensortec.com/bst/products/all_products/bsec),
which allows to read calibrated environment values including an actual Indoor
Air Quality (IAQ) score.

It makes use of
[Bosch's provided driver](https://github.com/BoschSensortec/BME680_driver)
and can be configured in terms of it.
Readings will be directly output to stdout in a loop.

## Prerequisites

[Download the BSEC software package from Bosch](https://www.bosch-sensortec.com/bst/products/all_products/bsec)
and put it into `./src`, then unpack.

Example :  
> cd ./src  
> wget https://www.bosch-sensortec.com/media/boschsensortec/downloads/bsec/bsec_1-4-8-0_generic_release.zip  
> unzip bsec_1-4-8-0_generic_release.zip  
> rm bsec_1-4-8-0_generic_release.zip  
> cd bsec_1-4-8-0_generic_release  
> wget https://github.com/BoschSensortec/BME680_driver/archive/bme680_v3.5.10.zip  
> mv BME680_driver-bme680_v3.5.10/ API  


## Configure and Compile

Optionally make changes to make.config.

Depending on how your sensor is embedded it might be surrounded by other
components giving off heat. Use an offset in °C in `bsec_bme680.c` to
compensate. The default is 5 °C:
```
#define temp_offset (5.0f)
```

To compile: `./make.sh`

## Usage

Output will be similar to this:

```
$ ./bsec_bme680
{"Localtime": "2020-11-14 22:55:43","IAQ_Accuracy": "3","IAQ":"245.41","Temperature": "15.30","Humidity": "84.98","Pressure": "1007.15","Gas": "33587","Status": "0","eCO2": "2652.58","bVOCe": "18.89"}  
{"Localtime": "2020-11-14 22:55:46","IAQ_Accuracy": "3","IAQ":"245.10","Temperature": "15.29","Humidity": "85.01","Pressure": "1007.13","Gas": "33534","Status": "0","eCO2": "2649.13","bVOCe": "18.79"}  
{"Localtime": "2020-11-14 22:55:49","IAQ_Accuracy": "3","IAQ":"244.77","Temperature": "15.29","Humidity": "85.03","Pressure": "1007.13","Gas": "33560","Status": "0","eCO2": "2645.51","bVOCe": "18.69"}  
```
* Localtime - Local system time
* IAQ_Accuracy - Accuracy of the IAQ score from 0 (low) to 3 (high).  
* IAQ - IAQ score (0-50 good || 51-100 average || 101-150 little bad || 151-200 bad || 201 –300 worse || 301 –500 very bad)  
* Temperature - Temperature value in Celsius
* Humidity - Humidity value in percent
* Pressure - Pressure value in hPa
* Gas - Gas value in Ohms
* Status - status of the sensors
* eCO2 - eCO2 value in ppm
* bVOCe - bVOCe value in ppm

It can easily be modified in the `output_ready` function.

The BSEC library is supposed to create an internal state of calibration with
increasing accuracy over time. Each 10.000 samples it will save the internal
calibration state to `./bsec_iaq.state` (or wherever you specify the config
directory to be) so it can pick up where it was after interruption.

## Sending JSON to InfluxDB

The output of the sensor can easily be sent directly to InfluxDB with python
Adjus the InfluxDB IP/Port and the mesurement field to your needs in read.py

Launch the python bridge:
`./read.py`

This can be automated launching `run.sh` using systemd unit file, with the below command  
> sudo useradd -r -G i2c -s /usr/sbin/nologin sensors  
> sudo mkdir /opt/bsec_bme680/  
> sudo cp ./bsec_bme680 /opt/bsec_bme680/  
> sudo cp bsec_bme680.logrotate /etc/logrotate.d/bsec_bme680  
> sudo cp run.sh /opt/bsec_bme680/  
> sudo cp bsec_bme680.service /lib/systemd/system/  
> sudo chown -R sensors:i2c /opt/bsec_bme680/  
> sudo chmod 744 /opt/bsec_bme680/run.sh  
> sudo touch /var/log/bsec_bme680.log  
> sudo chown sensors:i2c /var/log/bsec_bme680.log  
> sudo systemctl daemon-reload  
> sudo systemctl start bsec_bme680.service  
> systemctl status bsec_bme680.service  
> sudo systemctl enable bsec_bme680.service  

## Further

You can find a growing list of tools to further use and visualize the data
[here](https://github.com/alexh-name/bme680_outputs).

## Troubleshooting

### bsec_bme680 just quits without a message

Your bsec_iaq.state file might be corrupt or incompatible after an update of the
BSEC library. Try (re)moving it.

