#!/bin/bash

docker build -t alert-rules-proxy .
docker run -d -p 8000:8000 alert-rules-proxy

curl -X POST http://localhost:4443 \
   -H "Authorization: Bearer 123456" \
   -H "Content-Type: application/json" \
   -d '{"query": "A股指数"}'
