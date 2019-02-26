[![CircleCI](https://circleci.com/gh/sinofseven/sar-aws-sns-to-slack/tree/master.svg?style=svg)](https://circleci.com/gh/sinofseven/sar-aws-sns-to-slack/tree/master)

# aws-sns-to-slack

SNSトピックにSlackのimcomming_webhookにわたすJSONデータをPublishすると、Slackに投稿してくれるアプリケーションです。

SNSトピックはExportValueしているので、使う際にはそちらをImportしてください。

## 使い方
以下のようにSNSトピックにPublishしてください。

- Message: [必須] SlackのWebA API ```chat.postMessage```と同じ形式のJSON文字列
  - Messageの中身をそのままIncommingWebhookに投げているため
  - Slackのドキュメント
    - [Incoming Webhooks | Slack](https://api.slack.com/incoming-webhooks)
    - [chat.postMessage method | Slack (https://api.slack.com/methods/chat.postMessage)
- Subject: [オプション] IncommingWebhookのURLを指定する。指定されない場合はスタック作成時に登録したURLを使用する。

## CFnについて
- 使用しているParameter
  - ```DefaultSlackIncommingWebhookUrl```: [必須] デフォルトで使用するSlackのIncommingWebhookのURL
- Export-Value
  - ```${AWS::StackName}-SlackNotifierTopicArn```: SNSトピックのARN
  - ```${AWS::StackName}-SlackNotifierTopicArnParameterName```: SNSトピックのARNを格納したSSM Parameterの名前
  - ```${AWS::StackName}-SlackNotifierLayerArn```: 簡単にSNSにPublishでるように作成したLambda LayerのARN

## Lambda Layer

簡単にSNSにPublishできるようにLambda Layerも作ってみました。  
SNSにPublishする権限と、SSM Parameterから値を取得できる権限が必要になります。  
(SNS TopicのARNを直接指定する場合はSSM Parameterの閲覧権限は必要ありません)

### Python
Pythonの3.7, 3.6, 2.7に対応しています。  
以下のように書けば、使用可能になります。

```python
import aws_sns_to_slack
```

- easy_slack_notify()
- slack_notify()

#### ```easy_slack_notify(message, **args)```
渡したメッセージをSlackに投げるための簡素なメソッド。  
メッセージの他にはusernameとchannelしか指定できない。

```python
aws_sns_to_slack.easy_slack_notify(
    message,
    channel='string',
    username='string',
    incomming_webhook='string',
    ssm_parameter_name='string',
    topic_arn='string',
    sns_client=boto3.client('sns'),
    ssm_client=boto3.client('ssm')
)
```

- Parameters
  - **message** (*string*) --  
    **[REQUIRED]**  
    Slackに送るメッセージ。
  - **channel** (*string*) --  
    メッセージを送るチャンネルを指定する。  
    指定しなければ、incomming_webhookのDefault Channelになる。
  - **incomming_webhook** (*string*) --  
    Slackのincomming_webhookのURLを指定する。  
    指定しなければ、作成時に指定したDefaultのURLを使用する。
  - **ssm_parameter_name** (*string*) --  
    PublishするSNS TopicのARNを格納したSSM Parameterの名前を指定する。  
    指定しなければ、Default値```/sns-to-slack/SnsTopicArn```が指定される。
  - **topic_arn** (*string*) --  
    メッセージデータをPublishするSNS TopicのARN。  
    指定しなければSSM ParameterからARNを取得する。
  - **sns_client** (*boto3.client('sns')*) --  
    SNS TopicにPublishする際に使用するクライアント。  
    指定しなければ、```boto3.client('sns')```が使用される。
  - **ssm_client** (*boto3.client('ssm')*) --  
    SSM ParameterからSNS TopicのARNを取得する際に使用するクライアント。  
    指定しなければ、```boto3.client('ssm')```が使用される。


#### ```slack_notify(payload_json_text, **args)```
payload_json_textの内容をIncommingWebhookに投げる。

```python
aws_sns_to_slack.slack_notify(
    payload_json_text,
    incomming_webhook_url='string',
    ssm_parameter_name='string',
    topic_arn='string',
    sns_client=boto3.client('sns'),
    ssm_client=boto3.client('ssm')
)
```
- Parameters
  - **payload_json_text** (*string*) --  
    **[REQUIRED]**  
    Slackのincomming_webhookに渡すJSON文字列。  
    詳しくはSlackのドキュメントを参照して欲しい。
  - **incomming_webhook** (*string*) --  
    Slackのincomming_webhookのURLを指定する。  
    指定しなければ、作成時に指定したDefaultのURLを使用する。
  - **ssm_parameter_name** (*string*) --  
    PublishするSNS TopicのARNを格納したSSM Parameterの名前を指定する。  
    指定しなければ、Default値```/sns-to-slack/SnsTopicArn```が指定される。
  - **topic_arn** (*string*) --  
    メッセージデータをPublishするSNS TopicのARN。  
    指定しなければSSM ParameterからARNを取得する。
  - **sns_client** (*boto3.client('sns')*) --  
    SNS TopicにPublishする際に使用するクライアント。  
    指定しなければ、```boto3.client('sns')```が使用される。
  - **ssm_client** (*boto3.client('ssm')*) --  
    SSM ParameterからSNS TopicのARNを取得する際に使用するクライアント。  
    指定しなければ、```boto3.client('ssm')```が使用される。

## ローカルからデプロイする方法
```bash
$ S3_BUCKET=$(SAMのパッケージをアップロードするS3 Bucket) \
$ STACK_NAME=$(CloudFormationのスタック名) \
$ SLACK_INCOMMING_WEBHOOK_URL=$(デフォルトで使用するSlackのIncommingWebhookのURL) \
$ make deploy
```
