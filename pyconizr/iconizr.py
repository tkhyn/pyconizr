"""
Module that actually carries out the optimisation, spriting, conversion and CSS
generation
"""

import os
import shutil
import tempfile

from svg import SVGOpt, SVGSprite


TEMP_PREFIX = 'pyconizr-'


class Iconizr(object):

    def __init__(self, **options):

        self.options = options

        # copy the options as the instance's attributes
        self.src = options['in']

        self.tgt_css = options['out']

        self.tgt_sprite = options['out-sprite']
        sprite_path_end = os.path.split(self.tgt_sprite)[1]
        if '.' in sprite_path_end:
            self.sprite_name = os.path.splitext(sprite_path_end)
        else:
            self.sprite_name = os.path.split(self.src)[1].strip('/\\') + '.svg'
            self.tgt_sprite = os.path.join(self.tgt_sprite,
                                           self.sprite_name)

        self.css_format = options['css-fmt']

        # create a temp dir
        self.temp_dir = tempfile.mkdtemp(prefix=TEMP_PREFIX)
        self.temp_sprite = os.path.join(self.temp_dir, self.sprite_name)

        # parses the input directory and create SVG objects
        self.icons = []
        temp_src_dir = os.path.join(self.temp_dir,
                                    options['out-icons'] or 'icons')
        os.makedirs(temp_src_dir)
        for f in os.listdir(self.src):
            p_src = os.path.join(self.src, f)
            if os.path.isfile(p_src) \
            and os.path.splitext(f)[1].lower() == '.svg':
                p_temp = os.path.join(temp_src_dir, f)
                shutil.copy(p_src, p_temp)
                self.icons.append(SVGOpt(p_temp))

    def clean(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def iconize(self):
        """
        Executes all the tasks
        """

        tasks = ['optimize', 'spritize', 'makePNG', 'makeCSS', 'commit']
        for t in tasks:
            if not getattr(self, t)():
                return False
        return True

    def optimize(self):
        """
        Carry out optimisation on every SVG input file
        """

        success = True
        for icon in self.icons:
            if not icon.optimize(self.options):
                success = False

        return success

    def spritize(self):
        """
        Creates an SVG sprite from the SVG input file
        """

        # initialise, populate and save SVG sprite
        self.sprite = SVGSprite(self.temp_sprite, self.icons)
        self.sprite.populate()
        self.sprite.save(self.options)

        return True

    def makePNG(self):
        return True

    def makeCSS(self):
        return True

    def commit(self):
        # copy temporary files to destination
        shutil.copy(self.temp_sprite, self.tgt_sprite)

        icons_dir = self.options['out-icons']
        if icons_dir:
            # copy icons if required
            icons_temp_dir = os.path.join(self.temp_dir, icons_dir)
            icons_tgt_dir = os.path.join(self.tgt_sprite, icons_dir)
            for i in os.listdir(icons_temp_dir):
                shutil.copy(os.path.join(icons_temp_dir, i),
                            os.path.join(icons_tgt_dir, i))

        return True
