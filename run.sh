#!/bin/bash

pip install -e .

export APP_NAME=example-1
export ENV_NAME=prod
export AWS_DEFAULT_REGION=us-east-1

gunicorn -w 4 microblog.wsgi:app -b 0.0.0.0:5000