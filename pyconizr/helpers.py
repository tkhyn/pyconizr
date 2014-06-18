import re


def parseDim(dim):
    """
    Parses a dimension (float possibly concatenated with a unit)
    The unit must not be specified or be 'px'
    """
    m = re.match('^((?:\d+)?\.?(?:\d+))([a-z%]*)', dim)
    if m:
        l = m.groups()
        val = float(l[0]) if l[0] else False
        unit = l[1]
        if unit and unit != 'px':
            raise ValueError('Unit must be in px, %s found' % unit)
    else:
        val = False

    return val


def f2str(f):
    s = str(f)
    return s[-2:] == '.0' and s[:-2] or s
