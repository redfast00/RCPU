COMMENT_CHAR = ';'
LOCATIONS = ['{}.inc', 'include/{}.inc']


def remove_comments(lines):
    return [line for line in lines if not line.startswith(COMMENT_CHAR)]


def remove_whitespace(lines):
    return [line.strip() for line in lines if line.strip()]


def split_into_sections(lines):
    '''Splits lines into sections, expects lines to be sanitized.
       Also includes selected inc files.'''
    data = []
    text = []
    dataloc = find_index(lines, '.data')
    textloc = find_index(lines, '.text')

    if (dataloc is not None) and (textloc - dataloc > 1):
        data = lines[dataloc + 1:textloc]
    text = lines[textloc + 1:]
    # Include files here
    for line in lines[:textloc]:
        if line.startswith("include "):
            inc_data, inc_text = include_file(line.split(" ")[1])
            data.extend(inc_data)
            text.extend(inc_text)
    return data, text


def find_index(haystack, needle):
    try:
        loc = haystack.index(needle)
    except ValueError:
        return None
    return loc


def include_file(path):
    # TODO improve inc location finding
    for location in LOCATIONS:
        try:
            with open(location.format(path), 'r') as includefile:
                lines = includefile.readlines()
                return preprocess(lines)
        except IOError:
            continue
    else:
        raise IOError("Could not include {}".format(path))


def preprocess(lines):
    lines = remove_whitespace(lines)
    lines = remove_comments(lines)
    return split_into_sections(lines)
