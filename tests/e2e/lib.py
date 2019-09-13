import hashlib
import json
import time
from uuid import uuid4


def sleep():
    time.sleep(10)


def to_hash(key):
    return hashlib.sha3_256(key.encode()).hexdigest()


def create_key(prefix, item):
    return f"{prefix}{to_hash(json.dumps(item))}"


def get_object_text(s3_client, bucket, key, item):
    return s3_client.get_object(Bucket=bucket, Key=create_key(key, item))["Body"].read()


def lambda_invoke(lambda_client, function_name, event):
    options = {
        "FunctionName": function_name,
        "InvocationType": "RequestResponse",
        "Payload": json.dumps(event).encode("utf-8"),
    }
    resp = lambda_client.invoke(**options)
    if resp["StatusCode"] != 200:
        raise Exception("Lambda failed")


def create_list_expected():
    return [
        ({"text": f"test {uuid4()}"}),
        ({"user": "sinofseven", "message": f"Hello, World! {uuid4()}"}),
        ({"model": "nothung", "number": 11, "improvement": True, "name": f"須佐之男 {uuid4()}"}),
        (
            {
                "number": 21,
                "name": f"金剛 {uuid4()}",
                "type": "戦艦",
                "init": {"status": {"str": 63, "dex": 30}, "weapon": [7, 11, 37]},
            }
        ),
    ]


def create_test_data_for_layer_normal():
    return [
        ({"text": f"sinofseven {uuid4()}"}),
        ({"text": f"あなたは夜明けに微笑んで {uuid4()}", "channel": "#first"}),
        ({"text": f"奏でる少女の道行きは {uuid4()}", "username": "second"}),
        ({"text": f"アマデウスの詩、謳え敗者の王 {uuid4()}", "channel": "#third", "username": "third"}),
    ]


def create_test_data_for_layer_easy():
    data = []

    for raw_event, raw_expected in [
        ({"message": "sinofseven"}, {"text": "sinofseven"}),
        ({"message": "あなたは夜明けに微笑んで", "channel": "#first"}, {"text": "あなたは夜明けに微笑んで", "channel": "#first"}),
        ({"message": "奏でる少女の道行きは", "username": "second"}, {"text": "奏でる少女の道行きは", "username": "second"}),
        (
            {"message": "アマデウスの詩、謳え敗者の王", "channel": "#third", "username": "third"},
            {"text": "アマデウスの詩、謳え敗者の王", "channel": "#third", "username": "third"},
        ),
    ]:
        id = str(uuid4())
        event = {}
        expected = {}
        for k, v in raw_event.items():
            if k == "message":
                event[k] = f"{v} {id}"
            else:
                event[k] = v
        for k, v in raw_expected.items():
            if k == "text":
                expected[k] = f"{v} {id}"
            else:
                expected[k] = v
        data.append((event, expected))
    return data
