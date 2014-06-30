import os

from base import PyconizrTestCase

EXPECTED_PATH = os.path.join(os.path.dirname(__file__), 'expected')


class OutputTests(PyconizrTestCase):
    """
    Base output tests class
    """

    def setUp(self):
        super(OutputTests, self).setUp()
        # optimize SVGs, generate sprite and create an output file with default
        # settings
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makePNGs()
        self.iconizr.makeOutput()


class CSSTests(OutputTests):
    """
    Generate CSS files with default settings
    """

    options = {}

    def test_make_css(self):
        css_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.css')
        css_ref = os.path.join(EXPECTED_PATH, 'icons.css')
        self.assertSame(css_file, css_ref, mode='t')


class SCSSTests(OutputTests):
    """
    Generate SCSS files with default settings
    """

    options = {'render': 'scss'}

    def test_make_scss(self):
        scss_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.scss')
        scss_ref = os.path.join(EXPECTED_PATH, 'icons.scss')
        self.assertSame(scss_file, scss_ref, mode='t')


class SCSSTestsCommon(OutputTests):
    """
    Generate SCSS tests with a common class for all icons
    (Actually the CSS output should be the same)
    """

    options = {'render': 'scss', 'class': 'icons'}

    def test_scss_common(self):
        scss_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.scss')
        scss_ref = os.path.join(EXPECTED_PATH, 'icons-common.scss')
        self.assertSame(scss_file, scss_ref, mode='t')


class OutputPaddingTests(OutputTests):

    options = {'render': 'scss', 'padding': '2', 'class': 'icons'}

    def test_padding_output(self):

        scss_file = os.path.join(self.iconizr.temp_dir, 'out', 'icons.scss')
        scss_ref = os.path.join(EXPECTED_PATH, 'icons-padding.scss')
        self.assertSame(scss_file, scss_ref, mode='t')
