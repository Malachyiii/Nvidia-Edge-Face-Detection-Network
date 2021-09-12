docker build -t malachyiii/broker -f broker_Dockerfile .
docker push malachyiii/broker
docker build -t malachyiii/listener -f listener_Dockerfile .
docker push malachyiii/listener
docker build -t malachyiii/classifier -f classifier_Dockerfile .
sudo systemctl start k3s
export DISPLAY=:0
xhost +
kubectl apply -f mosquitto.yaml
kubectl apply -f mosquittoService.yaml
kubectl apply -f listener.yaml

