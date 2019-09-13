import os
import time

import boto3
import pytest


@pytest.fixture(scope="session")
def stack_name():
    return os.environ["STACK_NAME"]


@pytest.fixture(scope="session")
def cfn():
    return boto3.client("cloudformation")


@pytest.fixture(scope="session")
def lambda_client():
    return boto3.client("lambda")


@pytest.fixture(scope="session")
def sns():
    return boto3.client("sns")


@pytest.fixture(scope="session")
def s3_client():
    return boto3.client("s3")


@pytest.fixture(scope="session")
def s3_resource():
    return boto3.resource("s3")


@pytest.fixture(scope="session")
def stack_info(stack_name, cfn):
    resp = cfn.describe_stacks(StackName=stack_name)
    return resp["Stacks"][0]


@pytest.fixture(scope="session")
def stack_outputs(stack_info):
    result = {}
    for item in stack_info["Outputs"]:
        result[item["OutputKey"]] = item["OutputValue"]
    return result


@pytest.fixture(scope="session")
def sns_topic_arn(stack_outputs):
    return stack_outputs["SNSTopicArn"]


@pytest.fixture(scope="session")
def specific_url(stack_outputs):
    return stack_outputs["SpecificUrl"]


@pytest.fixture(scope="session")
def name_lambda_python36(stack_outputs):
    return stack_outputs["TestPython36LambdaFunctionArn"]


@pytest.fixture(scope="session")
def name_lambda_python37(stack_outputs):
    return stack_outputs["TestPython37LambdaFunctionArn"]


@pytest.fixture(scope="session")
def another_ssm_parameter_name(stack_outputs):
    return stack_outputs["AnotherNameTopicArnParameterName"]


@pytest.fixture(scope="session")
def tmp_bucket_name(stack_outputs):
    return stack_outputs["TmpBucketName"]


@pytest.fixture(scope="session")
def normal_key(stack_outputs):
    return stack_outputs["NormalKey"]


@pytest.fixture(scope="session")
def specific_key(stack_outputs):
    return stack_outputs["SpecificKey"]


@pytest.fixture(scope="function")
def delete_objects(request, s3_resource, tmp_bucket_name):
    def delete():
        bucket = s3_resource.Bucket(tmp_bucket_name)
        objs = bucket.objects.all()
        size = 0
        for obj in objs:
            size += 1
            obj.delete()
        time.sleep(size)

    request.addfinalizer(delete)
