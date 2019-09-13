import json

import pytest

from .lib import get_object_text, list_expected, sleep


@pytest.mark.usefixtures("delete_objects")
class TestDefaultUrl(object):
    @pytest.mark.parametrize("expected", list_expected)
    def test_expected(self, sns, sns_topic_arn, s3_client, tmp_bucket_name, normal_key, expected):
        sns.publish(TopicArn=sns_topic_arn, Message=json.dumps(expected))

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, normal_key)
        assert json.dumps(resp) == expected


@pytest.mark.usefixtures("delete_objects")
class TestSpecificUrl(object):
    @pytest.mark.parametrize("expected", list_expected)
    def test_expected(self, sns, sns_topic_arn, s3_client, tmp_bucket_name, specific_key, specific_url, expected):
        sns.publish(TopicArn=sns_topic_arn, Message=json.dumps(expected), Subject=specific_url)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, specific_key)
        assert json.dumps(resp) == expected
