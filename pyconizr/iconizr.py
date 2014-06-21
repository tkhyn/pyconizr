"""
Module that actually carries out the optimisation, spriting, conversion and
final output (css, sass, inline ...) generation
"""

import os
import shutil
import tempfile
from fnmatch import fnmatch

from img.svg import SVGIcon, SVGSprite


TEMP_PREFIX = 'pyconizr-'


class Iconizr(object):

    def __init__(self, **options):

        self.options = options

        # copy the options as the instance's attributes
        self.src = os.path.abspath(options['in'])

        if os.path.isdir(self.src):
            self.src_dir = self.src
            self.src_wildcard = '*'
        else:
            split = os.path.split(self.src)
            self.src_dir = split[0]
            self.src_wildcard = split[1]

            if not os.path.isdir(self.src_dir):
                raise ValueError(
                    'The specified input directory does not exist: %s'
                    % self.src_dir)

        self.tgt_sprite = options['out-sprite']
        sprite_path_end = os.path.split(self.tgt_sprite)[1]
        if '.' in sprite_path_end:
            self.sprite_name = os.path.splitext(sprite_path_end)
        else:
            self.sprite_name = os.path.split(self.src_dir)[1] + '.svg'
            self.tgt_sprite = os.path.join(self.tgt_sprite,
                                           self.sprite_name)

        out = os.path.abspath(self.options['out-path'])
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
        self.temp_sprite = os.path.join(self.temp_dir, 'sprites',
                                        self.sprite_name)

        # parses the input directory and create SVG objects
        self.icons = []
        temp_src_dir = os.path.join(self.temp_dir, options['out-icons-dir'])
        os.makedirs(temp_src_dir)
        for f in os.listdir(self.src_dir):
            p_src = os.path.join(self.src_dir, f)
            if os.path.isfile(p_src) \
            and fnmatch(f, self.src_wildcard) \
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
        try:
            os.makedirs(os.path.dirname(self.temp_sprite))
        except os.error:
            pass
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

        def copy_files(from_dir, to_dir):
            try:
                os.makedirs(to_dir)
            except os.error:
                pass
            for f in os.listdir(from_dir):
                f = os.path.join(from_dir, f)
                if os.path.isfile(f) \
                and (os.path.splitext(f)[1] != '.png'
                     or self.options['out-png']):
                    shutil.copy(f, to_dir)

        # copy main output files
        copy_files(os.path.join(self.temp_dir, 'out'),
                   self.out_dir)

        # copy png and SVG sprites
        copy_files(os.path.dirname(self.temp_sprite),
                   os.path.dirname(self.tgt_sprite))

        # copy individual icons if required
        if self.options['out-icons'] != 'no':
            icons_dir = self.options['out-icons-dir']
            icons_temp_dir = os.path.join(self.temp_dir, icons_dir)
            icons_tgt_dir = os.path.join(os.path.dirname(self.tgt_sprite),
                                         icons_dir)
            copy_files(icons_temp_dir, icons_tgt_dir)

        return True
