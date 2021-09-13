import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT=9001
LOCAL_MQTT_TOPIC="detected"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    print("message received",str(msg.payload))
    image = np.asarray(msg, dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print("image decoded")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()

