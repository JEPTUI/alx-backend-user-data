#!/usr/bin/env python3
"""Defines a function that returns the log message obfuscated"""


import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """Uses a regex to replace occurrences of certain field values"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
