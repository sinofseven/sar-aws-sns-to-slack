SHELL = /usr/bin/env bash -xeuo pipefail

E2E_TEST_STACK:=E2ETestStackForAWSSnsToSlack

lint:
	pipenv run flake8 \
		src/handlers/slack_notifier \
		tests/e2e/slack_notifier

isort:
	pipenv run isort -rc \
		src/handlers/slack_notifier \
		tests/e2e/slack_notifier

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

test-e2e:
	rm -rf .sam
	mkdir -p .sam
	pipenv run aws cloudformation package \
		--template-file e2e-template.yml \
		--s3-bucket $$S3_BUCKET \
		--output-template-file .sam/template.yml
	STACK_NAME=$(E2E_TEST_STACK) pipenv run pytest tests/e2e/test_e2e.py ;

.PHONY: \
	lint \
	isort \
	lsk-up \
	lsk-stop \
	lsk-down \
	deploy \
	build
