SHELL = /usr/bin/env bash -xeuo pipefail

E2E_TEST_STACK:=E2ETestStackForAWSSnsToSlack

lint:
	pipenv run flake8 \
		src/handlers/slack_notifier \
		src/layers/slack_notifier/ \
		tests/e2e/

isort:
	pipenv run isort -rc \
		src/handlers/slack_notifier \
		src/layers/slack_notifier \
		tests/e2e/

build:
	pwd_dir=$$PWD; \
	cd src/layers/requests; \
	pipenv lock --requirements > requirements.txt; \
	pip install -r requirements.txt -t python; \
	rm requirements.txt; \
	cd $$pwd_dir;

package:
	rm -rf .sam
	mkdir -p .sam
	pipenv run aws cloudformation package \
		--template-file sam.yml \
		--s3-bucket $$S3_BUCKET \
		--output-template-file .sam/template.yml

deploy: package
	pipenv run aws cloudformation deploy \
		--template-file .sam/template.yml \
		--stack-name $$STACK_NAME \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides DefaultSlackIncommingWebhookUrl=$$SLACK_INCOMMING_WEBHOOK_URL

destroy:
	pipenv run aws cloudformation delete-stack \
		--stack-name $$STACK_NAME
	pipenv run aws cloudformation wait stack-delete-complete \
		--stack-name $$STACK_NAME

test-e2e:
	STACK_NAME=$(E2E_TEST_STACK) pipenv run pytest tests/e2e/test_e2e.py ;

create-e2e-stack: build
	rm -rf .sam
	mkdir -p .sam
	pipenv run aws cloudformation package \
		--template-file e2e-template.yml \
		--s3-bucket $$S3_BUCKET \
		--output-template-file .sam/template.yml
	pipenv run aws cloudformation deploy \
		--template-file .sam/template.yml \
		--stack-name $(E2E_TEST_STACK) \
		--capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

delete-e2e-stack:
	pipenv run aws cloudformation delete-stack \
		--stack-name $(E2E_TEST_STACK)
	pipenv run aws cloudformation wait stack-delete-complete \
		--stack-name $(E2E_TEST_STACK)

.PHONY: \
	lint \
	isort \
	deploy \
	build \
	destroy \
	test-e2e \
	create-e2e-stack \
	delete-e2e-stack
