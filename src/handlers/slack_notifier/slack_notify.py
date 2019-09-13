import json
import os

import http_client as requests
from logger import get_logger

logger = get_logger(__name__)


class SlackNotifier(object):
    def __init__(self, event):
        self.event = event
        logger.info('event', self.event)

        self.url = os.environ['DEFAULT_INCOMMING_WEBHOOK_URL']
        logger.info('environ', {
            'DEFAULT_INCOMMING_WEBHOOK_URL': self.url
        })

    def main(self):
        self.parse_event()
        self.send_slack()

    def parse_event(self):
        sns = self.event['Records'][0]['Sns']
        payload = sns['Message']
        j_payload = json.loads(payload)
        logger.info('payload', payload)
        logger.info('payload(json)', j_payload)
        self.payload = payload

        url = sns['Subject']
        if isinstance(url, str) and len(url) > 0:
            self.url = url

    def send_slack(self):
        resp = requests.post(self.url, data=self.payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
        logger.info('post result', {
            'StatusCode': resp.status_code,
            'Headers': str(resp.headers),
            'Text': resp.read()
        })


def lambda_handler(event, context):
    try:
        os.environ['LAMBDA_REQUEST_ID'] = context.aws_request_id
        SlackNotifier(event).main()
    except Exception as e:
        logger.error(f'Exception occured: {e}', exc_info=True)
        raise e
