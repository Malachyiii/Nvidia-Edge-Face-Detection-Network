import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="detected"

REMOTE_MQTT_HOST="34.218.45.186"
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC="detected"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_connect_remote(client, userdata, flags, rc):
        print("connected to external broker with rc: " + str(rc))
        client.subscribe(REMOTE_MQTT_TOPIC)

messages = 0

def on_message(client,userdata, msg):
  global messages
  messages +=1
  try:
    print("messages received: " + str(messages))
    # if we wanted to re-publish this message, something like this should work
    msg = msg.payload
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    print("message sent")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

remote_mqttclient = mqtt.Client()
remote_mqttclient.on_connect = on_connect_remote
remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
remote_mqttclient.loop_start()

# go into a loop
local_mqttclient.loop_forever()
remote_mqttclient.loop_stop()
