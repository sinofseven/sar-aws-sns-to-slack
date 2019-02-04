import json

import pytest


def get_sqs_message(sqs, sqs_url, will_delete=True):
    resp = sqs.receive_message(QueueUrl=sqs_url, MaxNumberOfMessages=1)
    record = resp['Messages'][0]
    receipt_handle = record['ReceiptHandle']
    body = record['Body']
    if will_delete:
        sqs.delete_message(QueueUrl=sqs_url, ReceiptHandle=receipt_handle)
    return json.loads(body)


def lambda_invoke(lambda_client, function_name, event):
    options = {
        'FunctionName': function_name,
        'InvocationType': 'RequestResponse',
        'Payload': json.dumps(event).encode('utf-8')
    }
    resp = lambda_client.invoke(**options)
    if resp['StatusCode'] != 200:
        raise Exception('Lambda failed')


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

test_data = {
    'layer': {
        'slack_notify': [
            (
                {
                    'text': 'sinofseven'
                }
            ),
            (
                {
                    'text': 'あなたは夜明けに微笑んで',
                    'channel': '#first'
                }
            ),
            (
                {
                    'text': '奏でる少女の道行きは',
                    'username': 'second'
                }
            ),
            (
                {
                    'text': 'アマデウスの詩、謳え敗者の王',
                    'channel': '#third',
                    'username': 'third'
                }
            )
        ],
        'easy_slack_notify': [
            (
                {
                    'message': 'sinofseven'
                },
                {
                    'text': 'sinofseven'
                }
            ),
            (
                {
                    'message': 'あなたは夜明けに微笑んで',
                    'channel': '#first'
                },
                {
                    'text': 'あなたは夜明けに微笑んで',
                    'channel': '#first'
                }
            ),
            (
                {
                    'message': '奏でる少女の道行きは',
                    'username': 'second'
                },
                {
                    'text': '奏でる少女の道行きは',
                    'username': 'second'
                }
            ),
            (
                {
                    'message': 'アマデウスの詩、謳え敗者の王',
                    'channel': '#third',
                    'username': 'third'
                },
                {
                    'text': 'アマデウスの詩、謳え敗者の王',
                    'channel': '#third',
                    'username': 'third'
                }
            )
        ]
    }
}


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


class TestLayerPython36(object):
    @pytest.mark.parametrize(
        'expected', test_data['layer']['slack_notify']
    )
    def test_slack_notify_default(self, expected, lambda_client, name_lambda_python36, sqs, sqs_url):
        event = {
            'case': 'test_slack_notify_default',
            'data': expected
        }
        lambda_invoke(lambda_client, name_lambda_python36, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_default(self, data, expected, lambda_client, name_lambda_python36, sqs, sqs_url):
        event = {
            'case': 'test_easy_slack_notify_default',
            'data': data
        }
        lambda_invoke(lambda_client, name_lambda_python36, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_specific_url(self, data, expected, lambda_client, name_lambda_python36,
                                            sqs, sqs_url, specific_url):
        event = {
            'case': 'test_easy_slack_notify_specific_url',
            'data': data,
            'url': specific_url
        }
        lambda_invoke(lambda_client, name_lambda_python36, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'specific'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_parameter_name(self, data, expected, lambda_client, name_lambda_python36,
                                                  sqs, sqs_url, another_ssm_parameter_name):
        event = {
            'case': 'test_easy_slack_notify_set_parameter_name',
            'data': data,
            'ssm_parameter_name': another_ssm_parameter_name
        }

        lambda_invoke(lambda_client, name_lambda_python36, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_topic_arn(self, data, expected, lambda_client, name_lambda_python36,
                                             sqs, sqs_url, sns_topic_arn):
        event = {
            'case': 'test_easy_slack_notify_set_topic_arn',
            'data': data,
            'topic_arn': sns_topic_arn
        }

        lambda_invoke(lambda_client, name_lambda_python36, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected


class TestLayerPython37(object):
    @pytest.mark.parametrize(
        'expected', test_data['layer']['slack_notify']
    )
    def test_slack_notify_default(self, expected, lambda_client, name_lambda_python37, sqs, sqs_url):
        event = {
            'case': 'test_slack_notify_default',
            'data': expected
        }
        lambda_invoke(lambda_client, name_lambda_python37, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_default(self, data, expected, lambda_client, name_lambda_python37, sqs, sqs_url):
        event = {
            'case': 'test_easy_slack_notify_default',
            'data': data
        }
        lambda_invoke(lambda_client, name_lambda_python37, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_specific_url(self, data, expected, lambda_client, name_lambda_python37,
                                            sqs, sqs_url, specific_url):
        event = {
            'case': 'test_easy_slack_notify_specific_url',
            'data': data,
            'url': specific_url
        }
        lambda_invoke(lambda_client, name_lambda_python37, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'specific'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_parameter_name(self, data, expected, lambda_client, name_lambda_python37,
                                                  sqs, sqs_url, another_ssm_parameter_name):
        event = {
            'case': 'test_easy_slack_notify_set_parameter_name',
            'data': data,
            'ssm_parameter_name': another_ssm_parameter_name
        }

        lambda_invoke(lambda_client, name_lambda_python37, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_topic_arn(self, data, expected, lambda_client, name_lambda_python37,
                                             sqs, sqs_url, sns_topic_arn):
        event = {
            'case': 'test_easy_slack_notify_set_topic_arn',
            'data': data,
            'topic_arn': sns_topic_arn
        }

        lambda_invoke(lambda_client, name_lambda_python37, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected


class TestLayerPython27(object):
    @pytest.mark.parametrize(
        'expected', test_data['layer']['slack_notify']
    )
    def test_slack_notify_default(self, expected, lambda_client, name_lambda_python27, sqs, sqs_url):
        event = {
            'case': 'test_slack_notify_default',
            'data': expected
        }
        lambda_invoke(lambda_client, name_lambda_python27, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_default(self, data, expected, lambda_client, name_lambda_python27, sqs, sqs_url):
        event = {
            'case': 'test_easy_slack_notify_default',
            'data': data
        }
        lambda_invoke(lambda_client, name_lambda_python27, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_specific_url(self, data, expected, lambda_client, name_lambda_python27,
                                            sqs, sqs_url, specific_url):
        event = {
            'case': 'test_easy_slack_notify_specific_url',
            'data': data,
            'url': specific_url
        }
        lambda_invoke(lambda_client, name_lambda_python27, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'specific'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_parameter_name(self, data, expected, lambda_client, name_lambda_python27,
                                                  sqs, sqs_url, another_ssm_parameter_name):
        event = {
            'case': 'test_easy_slack_notify_set_parameter_name',
            'data': data,
            'ssm_parameter_name': another_ssm_parameter_name
        }

        lambda_invoke(lambda_client, name_lambda_python27, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected

    @pytest.mark.parametrize(
        'data, expected', test_data['layer']['easy_slack_notify']
    )
    def test_easy_slack_notify_set_topic_arn(self, data, expected, lambda_client, name_lambda_python27,
                                             sqs, sqs_url, sns_topic_arn):
        event = {
            'case': 'test_easy_slack_notify_set_topic_arn',
            'data': data,
            'topic_arn': sns_topic_arn
        }

        lambda_invoke(lambda_client, name_lambda_python27, event)

        body = get_sqs_message(sqs, sqs_url)

        assert body['Subject'] == 'default'
        assert json.loads(body['Message']) == expected
