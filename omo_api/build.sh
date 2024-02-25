#!/bin/bash

ECR_URL=187613313731.dkr.ecr.us-west-2.amazonaws.com
TAG=0.1.1

echo "Building Docker image..."

docker build -t omo_api:$TAG-amd64 -f Dockerfile.local --platform linux/amd64 .

#docker tag omo_api:$TAG $ECR_URL/omo_api:$TAG-amd64

echo "Pushing to ECR..."

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_URL 
docker push $ECR_URL/omo_api:$TAG-amd64

echo "Done."