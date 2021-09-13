ssh -A ubuntu@ec2-34-218-45-186.us-west-2.compute.amazonaws.com
cd ~/W251_Homework3
sudo su
docker build -t malachyiii/aws_broker -f aws_mqtt_Dockerfile .
docker push malachyiii/aws_broker
docker build -t malachyiii/processor -f processor_Dockerfile .
docker push malachyiii/processor
docker network create image-storage

docker run -d -it -p 1883:1883 -p 9001:9001 --network image-storage -v /home/ubuntu/W251_Homework3:/mosquitto/config/mosquitto.conf -v /home/ubuntu/W251_Homework3:/mosquitto/data -v /home/ubuntu/W251_Homework3/mosquitto/log:/mosquitto/log malachyiii/aws_broker
docker run -d -it --network image-storage malachyiii/processor
