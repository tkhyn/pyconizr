import os

from base import PyconizrTestCase

PNG_PATH = os.path.join(os.path.dirname(__file__), 'pngs')


class PNGTests(PyconizrTestCase):

    options = {'out-icons': True}

    def test_make_png(self):
        # optimize SVGs, generate sprite and create PNGs
        self.iconizr.optimize()
        self.iconizr.spritize()
        self.iconizr.makePNGs()

        png_sprite = os.path.splitext(self.iconizr.sprite.path)[0] + '.png'
        png_ref = os.path.join(PNG_PATH, os.path.split(png_sprite)[1])
        self.assertSame(png_sprite, png_ref)

        for icon in self.iconizr.icons:
            png_icon = os.path.splitext(icon.path)[0] + '.png'
            png_ref = os.path.join(PNG_PATH, os.path.split(png_icon)[1])
            self.assertSame(png_icon, png_ref)