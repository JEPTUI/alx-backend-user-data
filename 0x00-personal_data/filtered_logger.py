#!/usr/bin/env python3
"""Defines a function that returns the log message obfuscated"""


import re


def filter_datum(fields, redaction, message, separator):
    """Uses a regex to replace occurrences of certain field values"""
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message
