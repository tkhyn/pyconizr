"""
Module that actually carries out the optimisation, spriting, conversion and
final output (css, sass, inline ...) generation
"""

import os
import shutil
import tempfile
import glob

from six import iteritems

from .options import OPTIONS
from .img.svg import SVGIcon, SVGSprite


TEMP_PREFIX = 'pyconizr-'


class Iconizr(object):

    def __init__(self, **options):

        # check options and set defaults
        for o, param in iteritems(OPTIONS):
            option_name = param[1].get('dest', None) or o
            default_value = param[1].get('default', None)
            options.setdefault(option_name, default_value)
            if 'choices' in param[1]:
                assert options[option_name] in param[1]['choices']

        for url in ('sprites', 'icons'):
            opt = options[url + '-url']
            if opt.startswith('/') or ':' in opt:
                return
            else:
                opt = options['static-url'] + '/' + opt
            options[url + '-url'] = opt

        self.options = options

        # create a temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix=TEMP_PREFIX)

        # retrieve output sprite name and path
        self.tgt_sprite = options['out-sprite']
        sprite_path_end = os.path.split(self.tgt_sprite)[1]
        if '.' in sprite_path_end:
            # out-sprite is a filename
            self.sprite_name = sprite_path_end
        else:
            # out-sprite is a directory name, the sprite name and path will
            # be set on input files parsing
            self.sprite_name = None

        # parse input glob pattern(s) to collect icons
        paths = options['in']

        self.icons = []
        temp_src_dir = os.path.join(self.temp_dir,
                                    options['out-icons'] or 'icons')
        os.makedirs(temp_src_dir)

        def make_icon(path):
            name, ext = os.path.splitext(path)
            name = os.path.split(name)[1]
            if os.path.isfile(path) and ext == '.svg':
                # add file to icons
                p_temp = os.path.join(temp_src_dir, name + ext)
                i = 0
                while os.path.exists(p_temp):
                    p_temp = os.path.join(temp_src_dir,
                                          name + '-' + str(i) + ext)
                    i += 1
                shutil.copy(path, p_temp)
                self.icons.append(SVGIcon(p_temp))

                if not self.sprite_name:
                    # generate a sprite name and path from the first parsed
                    # file
                    self.sprite_name = \
                        os.path.split(os.path.dirname(path))[-1] + '.svg'
                    self.tgt_sprite = \
                        os.path.join(self.tgt_sprite, self.sprite_name)

        if hasattr(paths, '__iter__'):
            # input is an iterable (but not a string)
            for i in paths:
                make_icon(i)
        else:
            # input is a string
            globs = paths.split(',')
            for g in globs:
                matches = glob.glob(g)
                if len(matches) == 1 and os.path.isdir(matches[0]):
                    # the glob pattern refered to a single directory, we should
                    # understand it as directory/*
                    matches = glob.glob(os.path.join(g, '*'))
                for m in matches:
                    make_icon(m)

        if not self.icons:
            self.clean()
            raise Exception('No icon files found mathing pattern "%s"'
                            % options['in'])

        # create the temp sprite ...
        self.temp_sprite = os.path.join(self.temp_dir, 'sprites',
                                        self.sprite_name)
        # ... and the sprite object
        self.sprite = SVGSprite(self.temp_sprite, self.icons)

        # extract output directory and name
        out = os.path.abspath(self.options['out'])
        if '.' in out:
            out = os.path.split(out)
            self.out_name = out[1]
            self.out_dir = out[0]
        else:
            self.out_name = os.path.splitext(self.sprite_name)[0]
            self.out_dir = out

        # render mode
        self.render = options['render']
        if self.render in ('0', 'False', 'None'):
            self.render = None

        # valid selectors that can be embedded in filenames
        self.selectors = options['selectors'].split(',')

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
        self.sprite.populate(self)
        self.sprite.save(self)

        return True

    def makePNGs(self):

        if self.options['png']:
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
                     or self.options['png']):
                    shutil.copy(f, to_dir)

        # copy main output files if required
        if self.render:
            copy_files(os.path.join(self.temp_dir, 'out'),
                       self.out_dir)

        # copy png and SVG sprites
        copy_files(os.path.dirname(self.temp_sprite),
                   os.path.dirname(self.tgt_sprite))

        # copy individual icons if required
        if self.options['out-icons']:
            icons_dir = self.options['out-icons']
            icons_temp_dir = os.path.join(self.temp_dir, icons_dir)
            icons_tgt_dir = os.path.join(os.path.dirname(self.tgt_sprite),
                                         icons_dir)
            copy_files(icons_temp_dir, icons_tgt_dir)

        return True
