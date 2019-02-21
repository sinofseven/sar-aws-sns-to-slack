import os

import boto3
import pytest


@pytest.fixture(scope='session')
def stack_name():
    return os.environ['STACK_NAME']


@pytest.fixture(scope='session')
def cfn():
    return boto3.client('cloudformation')


@pytest.fixture(scope='session')
def sqs():
    return boto3.client('sqs')


@pytest.fixture(scope='session')
def lambda_client():
    return boto3.client('lambda')


@pytest.fixture(scope='session')
def sns():
    return boto3.client('sns')


@pytest.fixture(scope='session')
def stack_info(stack_name, cfn):
    resp = cfn.describe_stacks(StackName=stack_name)
    return resp['Stacks'][0]


@pytest.fixture(scope='session')
def stack_outputs(stack_info):
    result = {}
    for item in stack_info['Outputs']:
        result[item['OutputKey']] = item['OutputValue']
    return result


@pytest.fixture(scope='session')
def sns_topic_arn(stack_outputs):
    return stack_outputs['SNSTopicArn']


@pytest.fixture(scope='session')
def sqs_url(stack_outputs):
    return stack_outputs['SQSUrl']


@pytest.fixture(scope='session')
def specific_url(stack_outputs):
    return stack_outputs['SpecificUrl']


@pytest.fixture(scope='session')
def name_lambda_python36(stack_outputs):
    return stack_outputs['TestPython36LambdaFunctionArn']


@pytest.fixture(scope='session')
def name_lambda_python37(stack_outputs):
    return stack_outputs['TestPython37LambdaFunctionArn']


@pytest.fixture(scope='session')
def name_lambda_python27(stack_outputs):
    return stack_outputs['TestPython27LambdaFunctionArn']


@pytest.fixture(scope='session')
def another_ssm_parameter_name(stack_outputs):
    return stack_outputs['AnotherNameTopicArnParameterName']
