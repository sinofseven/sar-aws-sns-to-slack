import json
import logging
import logging.config
import os


class JsonLogFormatter(logging.Formatter):
    def format(self, record):
        result = {}

        for attr, value in record.__dict__.items():
            if attr == 'asctime':
                value = self.formatTime(record)
            if attr == 'exc_info' and value is not None:
                value = self.formatException(value)
            if attr == 'stack_info' and value is not None:
                value = self.formatStack(value)
            result[attr] = value

        result['lambda_request_id'] = os.environ['LAMBDA_REQUEST_ID']

        return json.dumps(result)


def get_logging_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'logFormatter': {
                '()': 'logger.JsonLogFormatter'
            }
        },
        'loggers': {
            'console': {
                'handlers': ['consoleHandler'],
                'level': 'DEBUG'
            },
            'botocore': {
                'handlers': ['consoleHandler'],
                'level': 'INFO'
            }
        },
        'handlers': {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'logFormatter'
            }
        },
        'root': {
            'handlers': ['consoleHandler'],
            'level': 'DEBUG'
        }
    }


def get_logger(name):
    logging.config.dictConfig(get_logging_config())
    return logging.getLogger(name)
