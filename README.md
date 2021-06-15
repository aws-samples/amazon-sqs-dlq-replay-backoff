# SQS dead letter queue replay with backoff and jitter

The theory behind the implementation is described in this article: [Exponential backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)

This serverless application deploys an Amazon SQS queue, linked with a dead letter queue (DLQ). An AWS lambda function replays each message of the DLQ with an exponential backoff and jitter. After some unsuccessful retries, messages are moved to a second DLQ.

## App Architecture

![Architecture diagram](SQS_replay.png)

## Installation Instructions

**Deploying the application with the Serverless Application Repository**

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one
1. Go to the app's page on the sqs-dlq-replay-backoff Serverless Application Repository page and click "Deploy"
1. Provide the required application parameters and click "Deploy"

**Deploying the application leveraging SAM (AWS Serverless Application Model):**

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one
1. Make sure to have [sam cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed.
1. Go to the directory you just cloned
1. Do a `sam build --use-container` (you need to have docker started)
1. Do a `sam --deploy guided` (it will help you go through the different steps and also parameters available in the stack to configure the jitter and backoff)


## Deployment Outputs

1. `ReplayFunction` - My Lambda function name, which replays SQS messages.
1. `MainQueueArn` - Main SQS queue.
1. `ReplayDeadLetterQueue` - Internal SQS dead letter queue.
1. `DeadLetterQueue`- SQS dead letter queue containing replayed messages still not processed

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
