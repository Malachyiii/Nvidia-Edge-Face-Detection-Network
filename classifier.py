import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt
import time

LOCAL_MQTT_HOST="classifier_service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="faces"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

cap = cv.VideoCapture(0)

while(cap.isOpened()==False):
    print("Waiting for connection...")
    time.sleep(5)

print("Video Connected...")

face_cascade = cv.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
print("Classifier Created")

while(True):
    ret, frame = cap.read()
    # gray here is the gray frame you will be getting from a camera
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    cv.imshow('frame',gray)
    for (x,y,w,h) in faces:
    	# your logic goes here; for instance
    	# cut out face from the frame..
        cv.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        cv.imshow('frame',gray)
        face = frame[y:y+h, x:x+w]
        rc,png = cv.imencode('.png', face)
        msg = png.tobytes()
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg)
    
    cv.imshow('frame',gray)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
