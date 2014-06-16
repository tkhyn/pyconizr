from options import OPTIONS
from iconizr import Iconizr


def _iconize(**options):
    """
    Wrapper function for the Iconizr.run method
    """

    iconizr = Iconizr(**options)

    try:
        result = iconizr.run()
        raise Exception
    except Exception, e:
        raise e
    finally:
        iconizr.clean()

    return result


def iconize(**options):
    """
    Public inconize function for use within python, check and set default
    options
    """

    for o, param in OPTIONS.iteritems():
        options.setdefault(param[1].get('dest', None)
                           or o, param[1]['default'])
    return _iconize(**options)


def execute_from_cl():
    import argparse

    parser = argparse.ArgumentParser(
        description='Pyconizr: SVG and PNG sprites from SVG files\n'
                    'Author: Thomas Khyn\n'
                    'Based on Iconizr by Joschi Kuphal')

    for o, param in OPTIONS.iteritems():
        parser.add_argument('--' + o, *param[0], **param[1])

    options = vars(parser.parse_args())
    _iconize(**options)
