"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import lambdalogging
import boto3
import config
import backoff

LOG = lambdalogging.getLogger(__name__)
SQS = boto3.client('sqs')


def handler(event, context):
    """Lambda function handler."""
    LOG.info('Received event: %s', event)
    LOG.debug('Main SQS queue ARN: %s', config.SQS_MAIN_URL)
    LOG.debug('Interval(s): %s', config.INTERVAL_SECONDS)
    LOG.debug('Max attemps: %s', config.MAX_ATTEMPS)
    LOG.debug('Backoff rate: %s', config.BACKOFF_RATE)
    LOG.debug('Message retention period: %s', config.MESSAGE_RETENTION_PERIOD)

    for record in event['Records']:
        nbReplay = 0
        # number of replay
        if 'sqs-dlq-replay-nb' in record['messageAttributes']:
            nbReplay = int(record['messageAttributes']['sqs-dlq-replay-nb']["stringValue"])

        LOG.info('Number of retries already done: %s', nbReplay)
        nbReplay += 1
        if nbReplay > config.MAX_ATTEMPS:
            raise MaxAttempsError(replay=nbReplay, max=config.MAX_ATTEMPS)

        # SQS attributes
        attributes = record['messageAttributes']
        attributes.update(
            {'sqs-dlq-replay-nb': {'StringValue': str(nbReplay), 'DataType': 'Number'}})

        LOG.debug("SQS message attributes: %s", attributes)
        _sqs_attributes_cleaner(attributes)
        LOG.debug("SQS message attributes cleaned: %s", attributes)

        # Backoff
        b = backoff.ExpoBackoffFullJitter(
            base=config.BACKOFF_RATE, 
            cap=config.MESSAGE_RETENTION_PERIOD)
        delaySeconds = b.backoff(n=int(nbReplay))

        # SQS
        msgreplay = "Message replayed to main SQS queue with delayseconds"
        LOG.info(msgreplay + "%s", delaySeconds)
        
        SQS.send_message(
            QueueUrl=config.SQS_MAIN_URL,
            MessageBody=record['body'],
            DelaySeconds=int(delaySeconds),
            MessageAttributes=record['messageAttributes']
        )


def _sqs_attributes_cleaner(attributes):
    """Transform SQS attributes from Lambda event to SQS message."""
    d = dict.fromkeys(attributes)
    for k in d:
        if isinstance(attributes[k], dict):
            subd = dict.fromkeys(attributes[k])
            for subk in subd:
                if not attributes[k][subk]:
                    del attributes[k][subk]
                else:
                    attributes[k][''.join(subk[:1].upper() + subk[1:])] = attributes[k].pop(subk)


class MaxAttempsError(Exception):
    """Raised when the max attempts is reached."""

    def __init__(self, replay, max, msg=None):
        """Init."""
        if msg is None:
            msg = "An error occured : " 
            "Number of retries(%s) is sup max attemps(%s)" % (replay, max)
        super(MaxAttempsError, self).__init__(msg)
        self.replay = replay
        self.max = max
