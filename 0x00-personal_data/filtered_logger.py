#!/usr/bin/env python3
"""
    Module for Filter_datum task
"""


import re


def match_field(message, field, reda):
    """matches field to replace"""
    for pos in range(len(message)):
        if field in message[pos]:
            pattern = field + '=(.)*'
            repl = field + '=' + reda
            return [pos, pattern, repl]


def filter_datum(fields, redaction, message, separator):
    """filters and logs message in obfuscated format"""
    mes_splited = message.split(separator)
    for field in fields:
        pos, pattern, repl = match_field(mes_splited, field, redaction)
        mes_splited[pos] = re.sub(pattern, repl, mes_splited[pos])
    return (separator.join(mes_splited))
