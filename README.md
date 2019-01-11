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
