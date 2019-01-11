SHELL = /usr/bin/env bash -xeuo pipefail

lint:
	pipenv run flake8 \
		./src/handler

isort:
	pipenv run isort -rc \
		src/handler

build:
	rm -rf .sam
	mkdir -p .sam
	pipenv run aws cloudformation package \
		--template-file sam.yml \
		--s3-bucket $$S3_BUCKET \
		--output-template-file .sam/template.yml

deploy: build
	pipenv run aws cloudformation deploy \
		--template-file .sam/template.yml \
		--stack-name $$STACK_NAME \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides DefaultSlackIncommingWebhookUrl=$$SLACK_INCOMMING_WEBHOOK_URL

.PHONY: \
	lint \
	isort \
	lsk-up \
	lsk-stop \
	lsk-down \
	deploy \
	build
