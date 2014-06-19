import os

from base import PyconizrTestCase

EXPECTED_PATH = os.path.join(os.path.dirname(__file__), 'expected')


class CSSTests(PyconizrTestCase):
    """
    Generate CSS files with default settings
    """

    options = {}

    def test_make_css(self):
        # optimize SVGs, generate sprite and create a CSS file with default
        # settings
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makeOutput()

        css_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.css')
        css_ref = os.path.join(EXPECTED_PATH, 'icons.css')
        self.assertSame(css_file, css_ref, mode='t')


class SCSSTests(PyconizrTestCase):
    """
    Generate SCSS files with default settings
    """

    options = {'out-fmt': 'scss'}

    def test_make_scss(self):
        # optimize SVGs, generate sprite and create a SCSS file with default
        # settings
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makeOutput()

        css_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.scss')
        css_ref = os.path.join(EXPECTED_PATH, 'icons.scss')
        self.assertSame(css_file, css_ref, mode='t')
