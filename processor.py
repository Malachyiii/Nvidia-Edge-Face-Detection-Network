import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST="aws_broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="detected"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
image_num = 0

def on_message(client,userdata, msg):
  global image_num
  try:
    print("message received")
    image = np.frombuffer(msg.payload, dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    print("image decoded")
    path = '/s3/'+str(image_num)+'.png'
    cv.imwrite(path, image, [cv.IMWRITE_PNG_COMPRESSION,4])
    image_num += 1
    print("image written")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()

