from six import iteritems

from .options import OPTIONS
from .iconizr import Iconizr


def iconize(**options):
    """
    Wrapper function for the Iconizr.run method
    """

    iconizr = Iconizr(**options)

    try:
        result = iconizr.iconize()
    except Exception as e:
        raise e
    finally:
        iconizr.clean()

    return result


def execute_from_cl():
    import argparse

    parser = argparse.ArgumentParser(
        description='Pyconizr: SVG and PNG sprites from SVG files\n'
                    'Author: Thomas Khyn\n'
                    'Inspiration taken from Iconizr by Joschi Kuphal',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    for o, param in iteritems(OPTIONS):
        parser.add_argument('--' + o, *param[0], **param[1])

    options = vars(parser.parse_args())
    iconize(**options)
