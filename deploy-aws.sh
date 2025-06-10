#!/bin/bash

# Build the SAM application
sam build

# Package the application using AWS CLI
aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket bedrock-artifatcs1234 \
    --output-template-file packaged.yaml

# Deploy the application using AWS CLI
aws cloudformation deploy \
    --template-file packaged.yaml \
    --stack-name bedrock-chat-app \
    --capabilities CAPABILITY_IAM \
    --region us-east-1
