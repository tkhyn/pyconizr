"""
Command line options tests
"""

import os

from ._base import PyconizrTestCase

from pyconizr.run import iconize
from pyconizr.options import ArgParser


class CmdLineTests(PyconizrTestCase):

    def pyconizr(self, *args):
        iconize(**dict(vars(ArgParser().parse_args(args)),
                       **self.iconizr.options))


class ArgsTests(CmdLineTests):

    def test_nopng(self):
        self.pyconizr('--nopng', '--out-icons', 'icons')

        png_sprite = os.path.splitext(self.iconizr.sprite.path)[0] + '.png'
        self.assertNotExists(png_sprite)

        for icon in self.iconizr.icons:
            self.assertNotExists(os.path.splitext(icon.path)[0] + '.png')
