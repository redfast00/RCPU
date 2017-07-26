COMMENT_CHAR = ';'

def remove_comments(lines):
    return [ line for line in lines if not line.startswith(COMMENT_CHAR) ]

def remove_whitespace(lines):
    return [ line.strip() for line in lines if line.strip()]

def split_into_sections(lines):
    '''Splits lines into sections, expects lines to be sanitized'''
    data = []
    text = []
    try:
        dataloc = lines.index(".data")
    except ValueError:
        dataloc = None
    textloc = lines.index(".text")

    if (dataloc is not None) and (textloc - dataloc > 1):
        data = lines[dataloc+1:textloc]
    text = lines[textloc+1:]
    return data, text

def preprocess(lines):
    lines = remove_whitespace(lines)
    lines = remove_comments(lines)
    return split_into_sections(lines)