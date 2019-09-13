import boto3
import os


def handler(event, context):
    boto3.client("s3").put_object(
        Bucket=os.environ["S3_BUCKET"],
        Key=os.environ["S3_KEY"],
        Body=event["body"].encode(),
        ContentType="application/json",
    )
    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}, "body": "success"}
