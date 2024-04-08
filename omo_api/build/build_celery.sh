#!/bin/bash

ECR_URL=$1
TAG=$2
IMAGE=omo_celery

echo "building with params $ECR_URL $TAG"
echo "Building Celery Docker image..."

docker build -t $IMAGE:$TAG-amd64 -f docker/Dockerfile.celery --platform linux/amd64 ..

docker tag $IMAGE:$TAG-amd64 $ECR_URL/$IMAGE:$TAG-amd64

echo "Pushing celery image to ECR..."

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_URL 
docker push $ECR_URL/$IMAGE:$TAG-amd64

echo "Done."