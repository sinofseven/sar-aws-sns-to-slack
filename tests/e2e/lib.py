import json
import time


def sleep():
    time.sleep(3)


def get_object_text(s3_client, bucket, key):
    return s3_client.get_object(Bucket=bucket, Key=key)["Body"].read()


def lambda_invoke(lambda_client, function_name, event):
    options = {
        "FunctionName": function_name,
        "InvocationType": "RequestResponse",
        "Payload": json.dumps(event).encode("utf-8"),
    }
    resp = lambda_client.invoke(**options)
    if resp["StatusCode"] != 200:
        raise Exception("Lambda failed")


list_expected = [
    ({"text": "test"}),
    ({"user": "sinofseven", "message": "Hello, World!"}),
    ({"model": "nothung", "number": 11, "improvement": True, "name": "須佐之男"}),
    ({"number": 21, "name": "金剛", "type": "戦艦", "init": {"status": {"str": 63, "dex": 30}, "weapon": [7, 11, 37]}}),
]

test_data = {
    "layer": {
        "slack_notify": [
            ({"text": "sinofseven"}),
            ({"text": "あなたは夜明けに微笑んで", "channel": "#first"}),
            ({"text": "奏でる少女の道行きは", "username": "second"}),
            ({"text": "アマデウスの詩、謳え敗者の王", "channel": "#third", "username": "third"}),
        ],
        "easy_slack_notify": [
            ({"message": "sinofseven"}, {"text": "sinofseven"}),
            ({"message": "あなたは夜明けに微笑んで", "channel": "#first"}, {"text": "あなたは夜明けに微笑んで", "channel": "#first"}),
            ({"message": "奏でる少女の道行きは", "username": "second"}, {"text": "奏でる少女の道行きは", "username": "second"}),
            (
                {"message": "アマデウスの詩、謳え敗者の王", "channel": "#third", "username": "third"},
                {"text": "アマデウスの詩、謳え敗者の王", "channel": "#third", "username": "third"},
            ),
        ],
    }
}
