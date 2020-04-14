# bsec_bme680_linux

Read the BME680 sensor with the BSEC library on Linux (e.g. Raspberry Pi)

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

Includes edits from [BME680 using the official Bosch Sensortec BSEC Library](https://community.home-assistant.io/t/bme680-using-the-official-bosch-sensortec-bsec-library/54103)

## Prerequisites

[Download the BSEC software package from Bosch](https://www.bosch-sensortec.com/bst/products/all_products/bsec) `wget https://www.bosch-sensortec.com/media/boschsensortec/downloads/bsec/bsec_1-4-7-4_generic_release.zip`
and put it into `./src`, then unpack `unzip bsec_1-4-7-4_generic_release.zip`.

## Configure and Compile

Optionally make changes to make.config.

Depending on how your sensor is embedded it might be surrounded by other
components giving off heat. Use an offset in °C in `bsec_bme680.c` to
compensate. Current value for my setup is 0.8 °C:
```
#define temp_offset (0.8f)
```

To compile: `./make.sh`

## Usage

Output will be similar to this:

```
$ ./bsec_bme680
{"IAQ_Accuracy": 0,"IAQ":25.00,"Temperature": 21.71,"Humidity": 39.26,"Pressure": 1009.72,"Gas": 96989,"bVOCe ppm": 0.5000,"Status": 0}
{"IAQ_Accuracy": 0,"IAQ":25.00,"Temperature": 21.71,"Humidity": 39.21,"Pressure": 1009.66,"Gas": 98240,"bVOCe ppm": 0.5000,"Status": 0}
{"IAQ_Accuracy": 0,"IAQ":25.00,"Temperature": 21.71,"Humidity": 39.23,"Pressure": 1009.68,"Gas": 98240,"bVOCe ppm": 0.5000,"Status": 0}
```
* IAQ (n) - Accuracy of the IAQ score from 0 (low) to 3 (high).
* S: n - Return value of the BSEC library

It can easily be modified in the `output_ready` function.

The BSEC library is supposed to create an internal state of calibration with
increasing accuracy over time. Each 10.000 samples it will save the internal
calibration state to `./bsec_iaq.state` (or wherever you specify the config
directory to be) so it can pick up where it was after interruption.

## Sending JSON to MQTT with Mostquitto

The output of the sensor can easily be sent to MQTT using Mosquitto
First, install Mosquitto Client `sudo apt-get install mosquitto-clients`

Launch the program and send the standard output to your Mosquitto broker
`./bsec_bme680 | mosquitto_pub -h 192.168.1.XXX -u "your broker user" -P "your broker password" -p 1883 -t home/pizero/bme680 -l`

## Further

You can find a growing list of tools to further use and visualize the data
[here](https://github.com/alexh-name/bme680_outputs).

## Troubleshooting

### bsec_bme680 just quits without a message

Your bsec_iaq.state file might be corrupt or incompatible after an update of the
BSEC library. Try (re)moving it.

