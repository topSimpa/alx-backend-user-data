#!/usr/bin/env python3
"""
    Module for Filter_datum task
"""

import logging
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """filters and logs message in obfuscated format"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return (message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filters incoming record before formatting"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

def get_logger() -> logging.Logger:
    """return logging.logger object at info level"""
    user_data = logging.get_logger('user_data')
    user_data.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormat(RedactingFormatter(PII_FIELDS))
    user_data.addHandler(handler)
    return (user_data)
