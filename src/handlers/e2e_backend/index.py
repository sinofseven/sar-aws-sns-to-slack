import boto3
import os
import hashlib


def to_hash(key):
    return hashlib.sha3_256(key.encode()).hexdigest()


def handler(event, context):
    boto3.client("s3").put_object(
        Bucket=os.environ["S3_BUCKET"],
        Key=f'{os.environ["S3_KEY"]}{to_hash(event["body"])}',
        Body=event["body"].encode(),
        ContentType="application/json",
    )
    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}, "body": "success"}
