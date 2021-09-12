docker build -t malachyiii/classifier -f classifier_Dockerfile .
docker push malachyiii/classifier
kubectl apply -f classifier.yaml
