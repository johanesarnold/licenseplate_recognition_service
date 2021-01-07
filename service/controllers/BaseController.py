from sqlalchemy import inspect
import sys, datetime, logging, traceback, json, difflib

#convert sql alchemy model to dict
def sqlAsDict(result):
    try:
        for row in result:
            return {c.key: getattr(row, c.key)
                    for c in inspect(row).mapper.column_attrs}
    except TypeError as te:
            return {c.key: getattr(result, c.key)
                    for c in inspect(result).mapper.column_attrs}

#compare 2 string and return ratio based from matched character
def compareString(expected, sample):
    #range 0 to 1 (1 if it's matched)
    seq = difflib.SequenceMatcher(a=expected.lower(), b=sample.lower())
    return seq.ratio() 
