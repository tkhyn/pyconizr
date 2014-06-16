import os
import shutil
from optparse import Values

from scour import scour
from options import SCOUR_OPTIONS


# patch scour
scour.unwanted_ns.extend([
    'http://creativecommons.org/ns#',  # Creative Commons
    'http://purl.org/dc/elements/1.1/',  # DublinCore
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#',  # RDF
])


class SVGObj(object):
    """
    Base class for SVG objects
    """

    def __init__(self, iconizr, path):
        self.temp_dir = iconizr.temp_dir
        self.path = path

    def optimize(self, options=None):

        if not options:
            options = {}

        for __, v in SCOUR_OPTIONS.values():
            options.setdefault(v['dest'], v['default'])

        scour.start(Values(options),
                    scour.maybe_gziped_file(self.path),
                    scour.maybe_gziped_file(self.path + 'opt', 'wb'))

        return True


class SVGFile(SVGObj):
    """
    An SVG input file
    """

    def __init__(self, iconizr, path):
        new_path = os.path.join(iconizr.temp_dir,
                                os.path.split(path)[1])
        super(SVGFile, self).__init__(iconizr, new_path)
        self.path_orig = path

        # copy the file to the temporary directory
        shutil.copy(path, new_path)


class SVGSprite(SVGObj):
    """
    An SVG sprite made from SVGObj SVG objects
    """
    pass
