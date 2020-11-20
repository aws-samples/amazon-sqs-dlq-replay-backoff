import pytest
import replay
import os
import json


@pytest.fixture
def mock_sqs(mocker):
    mocker.patch.object(replay, 'SQS')
    return replay.SQS


def test_handler(mocker, mock_sqs):
    full_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file = open(full_path + "/event_sqs_messages.json","r")
    event = file.read()
    event = json.loads(event)
    replay.handler(event, None)
    args, kwargs = mock_sqs.send_message.call_args
    print(kwargs)

    # test sqs message body is not modified
    assert "Hello world" == kwargs['MessageBody']
    # test backoff : delay seconds < message retention period
    assert int(kwargs['DelaySeconds']) < int(os.environ["MESSAGE_RETENTION_PERIOD"])
    # test sqs attributes is not modified
    assert set(('attr1', 'attr2')).issubset(kwargs['MessageAttributes'])
    # test number of replay : increment of sqs-dlq-replay-nb
    assert int(kwargs['MessageAttributes']['sqs-dlq-replay-nb']['StringValue']) == 2
