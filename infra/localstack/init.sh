#!/bin/bash
set -e

echo "Creating SQS queue and S3 bucket..."
awslocal sqs create-queue --queue-name docsense-jobs --region eu-west-3
awslocal s3 mb s3://docsense-documents --region eu-west-3
echo "LocalStack resources ready."