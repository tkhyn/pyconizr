from .iconizr import Iconizr
from .options import ArgParser


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
    parser = ArgParser()

    options = vars(parser.parse_args())
    iconize(**options)
