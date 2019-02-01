import json
from logging import getLogger

import boto3

ssm = boto3.client('ssm')
sns = boto3.client('sns')
logger = getLogger(__name__)
SSM_PARAMETER_NAME='/sns-to-slack/SnsTopicArn'


def get_sns_topic_arn(ssm_parameter_name=SSM_PARAMETER_NAME, ssm_client=ssm):
    logger.debug('ssm parameter name', ssm_parameter_name)
    resp = ssm_client.get_parameter(Name=ssm_parameter_name)
    return resp['Parameter']['Value']


def slack_notify(payload_json_text, incomming_webhook_url=None, topic_arn=None,
                 ssm_parameter_name=SSM_PARAMETER_NAME, sns_client=sns, ssm_client=ssm):
    options = {
        'Message': payload_json_text
    }
    if incomming_webhook_url is not None:
        options['Subject'] = incomming_webhook_url
    if topic_arn is None:
        options['TopicArn'] = get_sns_topic_arn(ssm_parameter_name=ssm_parameter_name, ssm_client=ssm_client)
    else:
        options['TopicArn'] = topic_arn

    logger.debug('sns publish options', options)
    sns_client.publish(**options)


def easy_slack_notify(message, channel=None, username=None, incomming_webhook_url=None,
                      topic_arn=None, ssm_parameter_name=SSM_PARAMETER_NAME, sns_client=sns, ssm_client=ssm):
    payload = {
        'text': message
    }
    if channel is not None:
        payload['channel'] = channel
    if username is not None:
        payload['username'] = username
    payload_text = json.dumps(payload)
    slack_notify(payload_text, incomming_webhook_url=incomming_webhook_url, topic_arn=topic_arn,
                 ssm_parameter_name=ssm_parameter_name, sns_client=sns_client, ssm_client=ssm_client)
