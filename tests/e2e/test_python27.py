import json

import pytest

from .lib import (create_test_data_for_layer_easy,
                  create_test_data_for_layer_normal, get_object_text,
                  lambda_invoke, sleep)


class TestLayerPython27(object):
    @pytest.mark.parametrize("expected", create_test_data_for_layer_normal())
    def test_slack_notify_default(
        self, expected, lambda_client, name_lambda_python27, s3_client, tmp_bucket_name, normal_key
    ):
        event = {"case": "test_slack_notify_default", "data": expected}
        lambda_invoke(lambda_client, name_lambda_python27, event)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, normal_key, expected)
        assert json.loads(resp) == expected

    @pytest.mark.parametrize("data, expected", create_test_data_for_layer_easy())
    def test_easy_slack_notify_default(
        self, data, expected, lambda_client, name_lambda_python27, s3_client, tmp_bucket_name, normal_key
    ):
        event = {"case": "test_easy_slack_notify_default", "data": data}
        lambda_invoke(lambda_client, name_lambda_python27, event)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, normal_key, expected)
        assert json.loads(resp) == expected

    @pytest.mark.parametrize("data, expected", create_test_data_for_layer_easy())
    def test_easy_slack_notify_specific_url(
        self,
        data,
        expected,
        lambda_client,
        name_lambda_python27,
        specific_url,
        s3_client,
        tmp_bucket_name,
        specific_key,
    ):
        event = {"case": "test_easy_slack_notify_specific_url", "data": data, "url": specific_url}
        lambda_invoke(lambda_client, name_lambda_python27, event)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, specific_key, expected)
        assert json.loads(resp) == expected

    @pytest.mark.parametrize("data, expected", create_test_data_for_layer_easy())
    def test_easy_slack_notify_set_parameter_name(
        self,
        data,
        expected,
        lambda_client,
        name_lambda_python27,
        another_ssm_parameter_name,
        s3_client,
        tmp_bucket_name,
        normal_key,
    ):
        event = {
            "case": "test_easy_slack_notify_set_parameter_name",
            "data": data,
            "ssm_parameter_name": another_ssm_parameter_name,
        }

        lambda_invoke(lambda_client, name_lambda_python27, event)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, normal_key, expected)
        assert json.loads(resp) == expected

    @pytest.mark.parametrize("data, expected", create_test_data_for_layer_easy())
    def test_easy_slack_notify_set_topic_arn(
        self, data, expected, lambda_client, name_lambda_python27, sns_topic_arn, s3_client, tmp_bucket_name, normal_key
    ):
        event = {"case": "test_easy_slack_notify_set_topic_arn", "data": data, "topic_arn": sns_topic_arn}

        lambda_invoke(lambda_client, name_lambda_python27, event)

        sleep()
        resp = get_object_text(s3_client, tmp_bucket_name, normal_key, expected)
        assert json.loads(resp) == expected
