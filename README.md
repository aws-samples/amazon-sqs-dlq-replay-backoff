# SQS dead letter replay

This serverless app deploys a SQS queue, linked with a dead letter queue (DLQ). A lambda function replays each message of the DLQ with an exponential backoff and jitter. After some unseccessful retries, messages are moved to a second DLQ.

## App Architecture

![Architecture diagram](SQS_replay.png)

## Installation Instructions

Choose if you want to deploy using the Serverless Application Repository or leveraging SAM (AWS Serverless Application Model):

<ins>A. Using  the Serverless Application Repository</ins>
1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to the app's page on the [sqs-dlq-replay Serverless Application Repository page](https://console.aws.amazon.com/serverlessrepo/home?region=eu-west-1#/published-applications/arn:aws:serverlessrepo:eu-west-1:862440218923:applications~sqs-dlq-replay) and click "Deploy"
1. Provide the required app parameters and click "Deploy"

<ins>B. Using sam within your local folder</ins>

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one
1. Make sure to have [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed.
1. Go to the directory you just cloned
1. Do a `sam --deploy guided` (it will help you go through the different steps and also parameters available in the stack to configure the jitter and backoff)



## Deployment Outputs

1. `ReplayFunction` - My Lambda function name, which replays SQS messages.
1. `MainQueueArn` - Main SQS queue.
1. `ReplayDeadLetterQueue` - Internal SQS dead letter queue.
1. `DeadLetterQueue`- SQS dead letter queue containing replayed messages still not processed

## License Summary

This code is made available under the MIT-0 license. See the LICENSE file.
