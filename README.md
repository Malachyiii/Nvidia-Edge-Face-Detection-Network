# Nvidia Edge Facial Detection

# Topic Questions:

1. Explain the topics and QoS used.

In order to streamline the process, only one topic was used throughout. This topic was labeled "detected", as in "face detected". Using this topic throughout allowed for bug checking of the actual data, and consistency in code prevented typos.

The QoS chosen was QoS = 0 or "at most once". This QoS was chosen due to the fact that the classifier is running at a relatively high frame rate. Even a few seconds of exposure creates many images. Using the "fire and forget" method keeps the publisher from getting bogged down with waiting for a response. There will more than likely be several copies of almost the same image sent, so any loss is trivial in this use case.


# Jetson Nano 2G

The architecture on the Nano 2G is as follows

- A Mosquitto server
- A listener at `listener.py`
- A republisher at `repub.py`
- A facial classifier built on top of the OpenCV framework at `classifier.py`

All 4 of these pieces are containerized and deployed into kubernetes. **The setup for these files can be accomplished by executing the** `run.sh` **shell script**. Teardown is accomplished via the `shutdown.sh` shell script.

Images for each of these pieces are contained in the respective Dockerfile

- Mosquitto server -> `broker_Dockerfile`
- Listener -> `listener_Dockerfile`
- Republisher -> `repub_Dockerfile`
- Facial classifier -> `classifier_Dockerfile`

And are deployed into Kubernetes with the appropriate YAML

- Mosquitto server -> `mosquitto.yaml`
- Listener -> `listener.yaml`
- Republisher -> `repub.yaml`
- Facial classifier -> `classifier.yaml`

The mosquitto server is then exposed with -> `mosquittoService.yaml`

`run.sh` is below for reference

```
docker build -t malachyiii/broker -f broker_Dockerfile .
docker push malachyiii/broker
docker build -t malachyiii/listener -f listener_Dockerfile .
docker push malachyiii/listener
docker build -t malachyiii/repub -f repub_Dockerfile .
docker push malachyiii/repub
docker build -t malachyiii/classifier -f classifier_Dockerfile .
docker push malachyiii/classifier
sudo systemctl start k3s
export DISPLAY=:0
xhost +
kubectl apply -f mosquitto.yaml
kubectl apply -f mosquittoService.yaml
kubectl apply -f classifier.yaml
kubectl apply -f listener.yaml
kubectl apply -f repub.yaml
```

## Flow

The flow of this cluster is as follows. An image classifier uses the local webcam to scan for faces. Upon detection it clips out the face and sends it in binary as a message to the mosquitto server on the topic "detected". From there it is picked up by the listener for logging purposes, and by the republisher, which passes it along to mqtt broker on the aws instance

#AWS Instance

After setting up the Amazon instance, the shell script `amazonsetup.sh` can be run to set up the receiving side.

The amazon setup involves 4 distinct steps:

1. tying the s3 bucket to a drive on the instance
2. building the docker images
3. creating the docker network
4. deploying the images into the network

The AWS instance is composed of 2 parts

-A Mosquitto server
-an image processor contained in processor.py

Both of these pieces are containerized and deployed into a docker network. **The setup for these containers is executed by the** `amazonsetup.sh` **shell script**.

Images for each of these pieces are contained in the respective Dockerfile

-Mosquitto server -> `aws_mqtt_Dockerfile`
-Image processor -> `processor_Dockerfile`

The script `amazonsetup.sh` is below

```
ssh -A ubuntu@ec2-34-218-45-186.us-west-2.compute.amazonaws.com
cd ~/W251_Homework3
sudo su

s3fs -o iam_role="HomeworkRole" -o url="https://s3-us-west-2.amazonaws.com" -o endpoint=us-west-2 -o dbglevel=info -o curldbg -o allow_other -o use_cache=/tmp w251homework3 /var/s3fs-homework

docker build -t malachyiii/aws_broker -f aws_mqtt_Dockerfile .
docker push malachyiii/aws_broker
docker build -t malachyiii/processor -f processor_Dockerfile .
docker push malachyiii/processor

docker network create image-storage

docker run -d --name aws_broker -it -p 1883:1883 --network image-storage -v /home/ubuntu/W251_Homework3:/mosquitto/config/mosquitto.conf -v /home/ubuntu/W251_Homework3:/mosquitto/data -v /home/ubuntu/W251_Homework3/mosquitto/log:/mosquitto/log malachyiii/aws_broker

sleep 10

docker run -d --privileged --name processor -i -v /var/s3fs-homework:/s3 --network image-storage malachyiii/processor
```

## Flow

The basic flow is as follows. Upon receiving a message from the Jetson side mqtt server a binary string of the image is published on the aws side on the topic "detected". The image processor picks this up over the `image-storage` docker network and publishes it to the mounted s3 bucket. 
