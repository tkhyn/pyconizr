import os

from base import PyconizrTestCase

CSS_PATH = os.path.join(os.path.dirname(__file__), 'css')


class CSSTests(PyconizrTestCase):

    options = {}

    def test_make_css(self):
        # optimize SVGs, generate sprite and create CSS
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makeCSS()

        css_file = os.path.join(self.iconizr.temp_dir, 'css', 'svgs.css')
        css_ref = os.path.join(CSS_PATH, 'default.css')
        self.assertSame(css_file, css_ref, mode='t')
