import json
import os

import boto3
import pytest


@pytest.fixture(scope='module')
def stack_name():
    return os.environ['STACK_NAME']


@pytest.fixture(scope='module')
def cfn():
    return boto3.client('cloudformation')


@pytest.fixture(scope='module', autouse=True)
def prepare_stack(stack_name, cfn):
    template = None
    with open('.sam/template.yml') as f:
        template = f.read()

    deploy = cfn.update_stack
    waiter = cfn.get_waiter('stack_update_complete')
    try:
        cfn.describe_stacks(StackName=stack_name)
    except:
        deploy = cfn.create_stack
        waiter = cfn.get_waiter('stack_create_complete')

    options = {
        'StackName': stack_name,
        'TemplateBody': template,
        'Capabilities': [
            'CAPABILITY_IAM',
            'CAPABILITY_AUTO_EXPAND'
        ]
    }
    deploy(**options)
    waiter.wait(StackName=stack_name)

    yield

    cfn.delete_stack(StackName=stack_name)
    cfn.get_waiter('stack_delete_complete').wait(StackName=stack_name)


@pytest.fixture(scope='module')
def sqs():
    return boto3.client('sqs')


@pytest.fixture(scope='module')
def sns():
    return boto3.client('sns')


@pytest.fixture(scope='module')
def stack_info(stack_name, cfn):
    resp = cfn.describe_stacks(StackName=stack_name)
    return resp['Stacks'][0]


@pytest.fixture(scope='module')
def stack_outputs(stack_info):
    result = {}
    for item in stack_info['Outputs']:
        result[item['OutputKey']] = item['OutputValue']
    return result


@pytest.fixture(scope='module')
def sns_topic_arn(stack_outputs):
    return stack_outputs['SNSTopicArn']


@pytest.fixture(scope='module')
def sqs_url(stack_outputs):
    return stack_outputs['SQSUrl']


@pytest.fixture(scope='module')
def specific_url(stack_outputs):
    return stack_outputs['SpecificUrl']


def get_sqs_message(sqs, sqs_url):
    resp = sqs.receive_message(QueueUrl=sqs_url, MaxNumberOfMessages=1)
    record = resp['Messages'][0]
    receipt_handle = record['ReceiptHandle']
    body = record['Body']
    sqs.delete_message(QueueUrl=sqs_url, ReceiptHandle=receipt_handle)
    return json.loads(body)


list_expected = [
    (
        {'text': 'test'}
    ),
    (
        {'user': 'sinofseven', 'message': 'Hello, World!'}
    ),
    (
        {'model': 'nothung', 'number': 11, 'improvement': True, 'name': '須佐之男'}
    ),
    (
        {
            'number': 21,
            'name': '金剛',
            'type': '戦艦',
            'init': {
                'status': {
                    'str': 63,
                    'dex': 30
                },
                'weapon': [
                    7,
                    11,
                    37
                ]
            }
        }
    )
]


def test_error():
    assert False


class TestDefaultUrl(object):
    @pytest.mark.parametrize('expected', list_expected)
    def test_expected(self, sns, sns_topic_arn, sqs, sqs_url, expected):
        sns.publish(TopicArn=sns_topic_arn, Message=json.dumps(expected))

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected


class TestSpecificUrl(object):
    @pytest.mark.parametrize('expected', list_expected)
    def test_expected(self, sns, sns_topic_arn, sqs, sqs_url, specific_url, expected):
        sns.publish(TopicArn=sns_topic_arn, Message=json.dumps(expected), Subject=specific_url)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'specific'
        assert json.loads(body['Message']) == expected
