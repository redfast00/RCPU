import re

def split_resource(line):
    '''
    Splits a line into references to resources and other text
    >>> split_resource("LDV A, .num")
    ["LDV A, ", ".num"]
    >>> split_resource("LDV A, (.test >> 6)")
    ["LDV A, (", ".test", " >> 6)"]
    '''
    expr = r'(\.[a-zA-Z0-9_]+|[^\.]+)'
    parts = re.findall(expr, line)
    return parts