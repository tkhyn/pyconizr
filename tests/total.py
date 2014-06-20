import os

from base import PyconizrTestCase


class TotalTests(PyconizrTestCase):

    def setUp(self):
        super(TotalTests, self).setUp()
        # optimize SVGs, generate sprite and create an output file with default
        # settings
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makePNGs()
        self.iconizr.makeOutput()
        self.iconizr.commit()


class DefaultTotalTests(TotalTests):

    options = {}

    def test_generate_files(self):
        out_dir = self.iconizr.options['out']
        self.assertListEqual(os.listdir(out_dir),
                             ['icons-png.css', 'icons.css', 'sprites'])
        self.assertListEqual(os.listdir(os.path.join(out_dir, 'sprites')),
                             ['icons.png', 'icons.svg'])

    def test_cleanup(self):
        self.iconizr.clean()
        self.assertNotExists(self.iconizr.temp_dir)
