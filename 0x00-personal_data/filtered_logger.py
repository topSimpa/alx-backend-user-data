#!/usr/bin/env python3
"""
    Module for Filter_datum task
"""


import re
from typing import List


def match_field(message: str, field: List, reda: str) -> List:
    """matches field to replace"""
    for pos in range(len(message)):
        if field in message[pos]:
            pattern: str = field + '=(.)*'
            repl: str = field + '=' + reda
            return [pos, pattern, repl]


def filter_datum(
        fields: List,
        redaction: str,
        message: str,
        separator: str) -> str:
    """filters and logs message in obfuscated format"""
    mes_splited: List = message.split(separator)
    for field in fields:
        pos, pattern, repl = match_field(mes_splited, field, redaction)
        mes_splited[pos] = re.sub(pattern, repl, mes_splited[pos])
    return (separator.join(mes_splited))
