#!/bin/bash

ECR_URL=187613313731.dkr.ecr.us-west-2.amazonaws.com
TAG=v0.4.13


function authenticate_image_registry() {
    aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ECR_URL    
}
    
function build_image() {
    docker build -t $IMAGE:$TAG-amd64 -f Dockerfile --target $TARGET --platform linux/amd64 ../
    docker tag $IMAGE:$TAG-amd64 $ECR_URL/$IMAGE:$TAG-amd64
}

function push_image() {
    docker push $ECR_URL/$IMAGE:$TAG-amd64
}

function build_and_push_api() {
    IMAGE=omo_api
    TARGET=api
    echo "Building API Docker image..."
    build_image
    
    echo "Pushing image to ECR..."
    authenticate_image_registry
    push_image
}

function build_and_push_celeryworker() {
    IMAGE=omo_celery
    TARGET=celeryworker
    echo "Building celery worker image..."
    build_image

    echo "Pushing image to ECR..."
    authenticate_image_registry
    push_image

}

function build_and_push_celerybeat() {
    IMAGE=omo_celery_beat
    TARGET=celerybeat
    echo "Building celerybeat image..."
    build_image

    echo "Pushing image to ECR..."
    authenticate_image_registry
    push_image
}

build_and_push_api
build_and_push_celeryworker
build_and_push_celerybeat