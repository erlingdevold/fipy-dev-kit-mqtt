from telenor import StartIoT
from mqtt import MQTTClient
from uos import urandom
from ujson import dumps
from time import sleep


# Amazon Web Services (AWS) IoT configuration
AWS_PORT = 8883
AWS_HOST = 'a15nxxwvsld4o-ats.iot.eu-west-1.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/root.pem'
AWS_CLIENT_CERT = '/flash/cert/cert.pem'
AWS_PRIVATE_KEY = '/flash/cert/privkey.pem'

# Your Telenor Managed IoT Cloud (MIC) Thing configuration.
# Change this to your Thing name / ID:
THING_ID = ''

# MQTT configuration
MQTT_TOPIC = '$aws/things/' + THING_ID + '/shadow/update'

def sub_callback(topic, msg):
  print(msg)

def run():
  
  # Create a new Telenor Start IoT object using the LTE-M network.
  # Change the `network` parameter if you want to use the NB-IoT
  # network like this: iot = StartIoT(network='nb-iot')
  # You must flash the correct Sequans modem firmware before
  # changing network protocol!
  iot = StartIoT(network='lte-m')

  # Connect to the network
  print("Started connecting to the network...")
  iot.connect()

  # We should now be connected.
  # Setup an MQTT client using our certificates and keys.
  client = MQTTClient(
    client_id=THING_ID, server=AWS_HOST,
    port=AWS_PORT, keepalive=10000,
    ssl=True, ssl_params={
      'certfile': AWS_CLIENT_CERT,
      'keyfile': AWS_PRIVATE_KEY,
      'ca_certs': AWS_ROOT_CA
    })

  # Set callback function, connect, and subscribe to MIC Thing topic
  client.set_callback(sub_callback)
  client.connect()
  client.subscribe(MQTT_TOPIC)

  # Start an endless loop and publish some dummy data over MQTT.
  while True:

    try:
      # Generate random data
      temperature = ((urandom(1)[0] / 256) * 10) + 20
      humidity = ((urandom(1)[0] / 256) * 10) + 60

      # Create the MQTT data payload
      payload = {
        'state': {
          'reported': {
            'temperature': temperature,
            'humidity': humidity
          }
        }
      }

      # Format payload as a JSON string
      json = dumps(payload)

      print('Sending data:', json)

      # Publish JSON string over the network
      client.publish(topic=MQTT_TOPIC, msg=json, qos=0)

    # Handle exception (if an error occured)
    except Exception as e:
      print('Caugh exception:', e)

    # Wait 10 seconds before running loop again
    sleep(10)

    # Check if we got a downlink message from the MQTT broker
    client.check_msg()

# The example code will start here
print('Running example code...')
run()
