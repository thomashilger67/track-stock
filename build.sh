#!/bin/bash

docker build -t track-stock --build-arg TICKERS .
docker tag track-stock:latest 156999051389.dkr.ecr.eu-north-1.amazonaws.com/registry/track-stock:latest
docker push 156999051389.dkr.ecr.eu-north-1.amazonaws.com/registry/track-stock:latest