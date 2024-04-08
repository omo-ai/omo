#!/bin/bash

ECR_URL=$1
TAG=$2
IMAGE=omo_celery_beat

echo "Building celery beat Docker image..."

docker build -t $IMAGE:$TAG-amd64 -f docker/Dockerfile.celerybeat --platform linux/amd64 ../

docker tag $IMAGE:$TAG-amd64 $ECR_URL/$IMAGE:$TAG-amd64

echo "Pushing celery beat image to ECR..."

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_URL 
docker push $ECR_URL/$IMAGE:$TAG-amd64

echo "Done."