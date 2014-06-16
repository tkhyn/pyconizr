"""
Module that actually carries out the optimisation, spriting, conversion and CSS
generation
"""

import os
import shutil
import tempfile

from svg import SVGFile, SVGSprite


TEMP_PREFIX = 'iconizr'


class Iconizr(object):

    def __init__(self, **options):

        # copy the options as the instance's attributes
        self.src = options['in']

        self.tgt_css = options['out']
        self.tgt_sprite = options['out-sprite']

        self.css_format = options['css-fmt']

        # create a temp dir
        self.temp_dir = tempfile.mkdtemp(prefix=TEMP_PREFIX)

        # parses the input directory and create SVG objects
        self.svg_in = []
        for f in os.listdir(self.src):
            p = os.path.join(self.src, f)
            if os.path.isfile(p) and os.path.splitext(f)[1].lower() == '.svg':
                self.svg_in.append(SVGFile(self, p))

    def clean(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def iconize(self):
        """
        Executes all the tasks
        """

        tasks = ['optimize', 'sprite', 'makePNG', 'makeCSS']
        for t in tasks:
            if not getattr(self, t)():
                return False
        return True

    def optimize(self):
        """
        Carry out optimisation on every SVG input file
        """

        success = True
        for svg_file in self.svg_in:
            if not svg_file.optimize():
                success = False

        return success

    def sprite(self):
        """
        Creates an SVG sprite from the SVG input file
        """
        return True

    def makePNG(self):
        return True

    def makeCSS(self):
        return True
