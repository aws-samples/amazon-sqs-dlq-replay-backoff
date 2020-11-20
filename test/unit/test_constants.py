"""Constants used for unit tests.

This can be used to define values for environment variables so unit tests can use these to assert on expected values.
"""

import os

os.environ["LOG_LEVEL"] = 'DEBUG'
os.environ["SQS_MAIN_URL"] = 'https://sqs.mock.mock'
os.environ["INTERVAL_SECONDS"] = '2'
os.environ["MAX_ATTEMPS"] = '3'
os.environ["BACKOFF_RATE"] = '2'
os.environ["MESSAGE_RETENTION_PERIOD"] = '1000'
