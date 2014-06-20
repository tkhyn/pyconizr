"""
Module that actually carries out the optimisation, spriting, conversion and
final output (css, sass, inline ...) generation
"""

import os
import shutil
import tempfile

from img.svg import SVGIcon, SVGSprite


TEMP_PREFIX = 'pyconizr-'


class Iconizr(object):

    def __init__(self, **options):

        self.options = options

        # copy the options as the instance's attributes
        self.src = options['in']

        self.tgt_sprite = options['out-sprite']
        sprite_path_end = os.path.split(self.tgt_sprite)[1]
        if '.' in sprite_path_end:
            self.sprite_name = os.path.splitext(sprite_path_end)
        else:
            self.sprite_name = os.path.split(self.src)[1].strip('/\\') + '.svg'
            self.tgt_sprite = os.path.join(self.tgt_sprite,
                                           self.sprite_name)

        out = self.options['out']
        if '.' in out:
            out = os.path.split(out)
            self.out_name = out[1]
            self.out_dir = out[0]
        else:
            self.out_name = os.path.splitext(self.sprite_name)[0]
            self.out_dir = out

        # icons dir
        self.tgt_icons_dir = os.path.join(os.path.dirname(self.tgt_sprite),
                                          options['out-icons-dir'])

        # create a temp dir
        self.temp_dir = tempfile.mkdtemp(prefix=TEMP_PREFIX)
        self.temp_sprite = os.path.join(self.temp_dir, self.sprite_name)

        # parses the input directory and create SVG objects
        self.icons = []
        temp_src_dir = os.path.join(self.temp_dir, options['out-icons-dir'])
        os.makedirs(temp_src_dir)
        for f in os.listdir(self.src):
            p_src = os.path.join(self.src, f)
            if os.path.isfile(p_src) \
            and os.path.splitext(f)[1].lower() == '.svg':
                p_temp = os.path.join(temp_src_dir, f)
                shutil.copy(p_src, p_temp)
                self.icons.append(SVGIcon(p_temp))

    def clean(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def iconize(self):
        """
        Executes all the tasks
        """

        tasks = ['optimize', 'spritize', 'makePNGs', 'makeOutput', 'commit']
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
            if not icon.optimize(self):
                success = False

        return success

    def spritize(self):
        """
        Creates an SVG sprite from the SVG input file
        """

        # initialise, populate and save SVG sprite
        self.sprite = SVGSprite(self.temp_sprite, self.icons)
        self.sprite.populate()
        self.sprite.save(self)

        return True

    def makePNGs(self):

        if self.options['out-png']:
            # make sprite png
            self.sprite.makePNG()

            # make icons png if required
            if self.options['out-icons']:
                for icon in self.icons:
                    icon.makePNG()

            return True

    def makeOutput(self):
        self.sprite.makeOutput(self)
        return True

    def commit(self):
        # copy temporary files to destination
        shutil.copy(self.temp_sprite, self.tgt_sprite)

        if self.options['out-icons']:
            # copy icons if required
            icons_dir = self.options['out-icons-dir']
            icons_temp_dir = os.path.join(self.temp_dir, icons_dir)
            icons_tgt_dir = os.path.join(self.tgt_sprite, icons_dir)
            for i in os.listdir(icons_temp_dir):
                shutil.copy(os.path.join(icons_temp_dir, i),
                            os.path.join(icons_tgt_dir, i))

        return True
