#!/bin/bash

# Build the SAM application
sam build

# Package the application
sam package \
    --s3-bucket bedrock-chat-app-deploy \
    --output-template-file packaged.yaml

# Deploy the application
sam deploy \
    --template-file packaged.yaml \
    --stack-name bedrock-chat-app \
    --capabilities CAPABILITY_IAM \
    --region us-east-1
