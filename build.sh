#!/bin/bash

docker build -t alert-rules-proxy .
docker run -d -p 8000:8000 alert-rules-proxy
