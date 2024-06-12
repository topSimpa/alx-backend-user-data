#!/usr/bin/env python3
"""
    Module for Filter_datum task
"""

import bcrypt
import logging
import mysql.connector
import os
import re
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return (logger)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connects to the database and returns a connector object"""
    connector = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        passwd=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.environ["PERSONAL_DATA_DB_NAME"]
    )
    return (connector)


def main():
    """Obtains a database connection using get_db and
        retrieve all rows in the users table and
        display each row under a filtered format
    """

    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users;"
    )
    result = cursor.fetchall()

    for row in result:
        data = {
            "name": f"name={row[0]}; ",
            "email": f"email={row[1]}; ",
            "phone": f"phone={row[2]}; ",
            "ssn": f"ssn={row[3]}; ",
            "password": f"password={row[4]}; ",
            "ip": f"ip={row[5]}; ",
            "last_login": f"last_login={row[6]}; ",
            "user_agent": f"user_agent={row[7]};"
        }
        line = data['name'] + data['email'] + data['phone'] + \
            data['ssn'] + data['password'] + data['ip'] + \
            data['last_login'] + data['user_agent']

        logger.info(line)
    cursor.close()


if __name__ == '__main__':
    main()
