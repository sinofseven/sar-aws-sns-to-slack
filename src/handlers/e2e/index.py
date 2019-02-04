from aws_sns_to_slack import slack_notify, easy_slack_notify
from logger import get_logger
import json

logger = get_logger(__name__)

def test_slack_notify_default(test_data):
    slack_notify(json.dumps(test_data))


def test_easy_slack_notify_default(test_data):
    message = test_data.get('message')
    channel = test_data.get('channel')
    username = test_data.get('username')
    easy_slack_notify(message, channel=channel, username=username)


def test_easy_slack_notify_specific_url(event):
    test_data = event.get('data', {})
    message = test_data.get('message')
    channel = test_data.get('channel')
    username = test_data.get('username')
    url = event.get('url')
    easy_slack_notify(message, channel=channel, username=username, incomming_webhook_url=url)

def test_easy_slack_notify_set_parameter_name(event):
    test_data = event.get('data', {})
    message = test_data.get('message')
    channel = test_data.get('channel')
    username = test_data.get('username')
    parameter_name = event.get('ssm_parameter_name')
    easy_slack_notify(message, channel=channel, username=username, ssm_parameter_name=parameter_name)

def test_easy_slack_notify_set_topic_arn(event):
    test_data = event.get('data', {})
    message = test_data.get('message')
    channel = test_data.get('channel')
    username = test_data.get('username')
    topic_arn = event.get('topic_arn')
    easy_slack_notify(message, channel=channel, username=username, topic_arn=topic_arn)

def lambda_handler(event, content):
    logger.info('event', event)
    case = event['case']
    data = event['data']

    if case == 'test_slack_notify_default':
        test_slack_notify_default(data)
    elif case == 'test_easy_slack_notify_default':
        test_easy_slack_notify_default(data)
    elif case == 'test_easy_slack_notify_specific_url':
        test_easy_slack_notify_specific_url(event)
    elif case == 'test_easy_slack_notify_set_parameter_name':
        test_easy_slack_notify_set_parameter_name(event)
    elif case == 'test_easy_slack_notify_set_topic_arn':
        test_easy_slack_notify_set_topic_arn(event)
    else:
        raise ValueError()
