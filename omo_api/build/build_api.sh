#!/bin/bash

ECR_URL=$1
TAG=$2
IMAGE=omo_api

echo "Building API Docker image..."

docker build -t $IMAGE:$TAG-amd64 -f docker/Dockerfile.api --platform linux/amd64 .

docker tag $IMAGE:$TAG-amd64 $ECR_URL/$IMAGE:$TAG-amd64

echo "Pushing API to ECR..."

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_URL 
docker push $ECR_URL/$IMAGE:$TAG-amd64

echo "Done."