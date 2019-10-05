# FiPy Dev-Kit MQTT Example Code

The example publishes data packets over LTE-M (Cat M1) or NB-IoT network to Telenor Start IoT Managed IoT Cloud (MIC) using the MQTT protocol.

## Prerequsites

Your Pycom FiPy dev-kit contains a Sequans modem. This modem needs to be flashed with firmware for the correct network protocol (LTE-M or NB-IoT). This must be done before you try to connect using the selected network protocol. The Sequans modem is by default flashed for LTE-M, so if you plan to use LTE-M you can skip this step.

Instructions on how to update or flash a different FiPy Sequans modem firmware can be found in the Pycom documentation here: https://docs.pycom.io/tutorials/lte/firmware/

## Change Network Protocol

The code will by default use the LTE-M network:

``` python
iot = StartIoT(network='lte-m')
```

To use the NB-IoT network (assuming you have flashed the modem as described in the prerequisites):

``` python
iot = StartIoT(network='nb-iot')
```

## Network Related Code Changes

The code in this repository reflects settings for the network in Telenor Norway. If your device will connect to a different network you will have to make some changes in [lib/telenor.py:11](./lib/telenor.py#L11) to reflect this:

``` python
# Network related configuration
BAND = 20                 # Telenor NB-IoT band frequency
APN = 'telenor.iot'       # Telenor public IoT on 4G APN
IOTGW_IP = ''             # Telenor IoT Gateway IP address
EARFCN = 6352             # Telenor E-UTRA Absolute Radio Frequency Channel Number
COPS = 24201              # Telenor network shortname
```

Notice that since the MQTT broker is operated by Amazon Web Services (AWS) you must use the public Telenor IoT on 4G APN **telenor.iot**.
