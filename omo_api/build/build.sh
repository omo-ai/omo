#!/bin/bash

ECR_URL=187613313731.dkr.ecr.us-west-2.amazonaws.com
TAG=0.2.1

./build_api.sh $ECR_URL $TAG
./build_celery.sh $ECR_URL $TAG
./build_celerybeat.sh $ECR_URL $TAG