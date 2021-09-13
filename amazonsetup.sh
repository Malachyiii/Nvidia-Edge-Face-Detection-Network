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
