kubectl delete service mosquitto-service
kubectl delete deployment classifier-deployment listener-deployment mosquitto-deployment repub-deployment
sleep 30
sudo systemctl stop k3s
