from lxml import etree as ET

from base import PyconizrTestCase


class SpritizeTests(PyconizrTestCase):

    options = {}

    def test_spritize_3_files(self):

        # optimize first, so that we have clean SVG
        self.iconizr.optimize()
        self.iconizr.spritize()

        self.assertExists(self.iconizr.temp_sprite)

        sprite_root = ET.parse(self.iconizr.temp_sprite).getroot()
        self.assertEqual(sprite_root.tag, self.nstag('svg'))
        self.assertEqual(sprite_root.get('width'), '32px')
        self.assertEqual(sprite_root.get('height'), '96px')
        self.assertEqual(sprite_root.get('viewBox'), '0 0 32 96')

        for icon in sprite_root:
            if icon.get('id') == 'red-triangle':
                self.assertEqual(icon.get('y'), '0')
            elif icon.get('id') == 'yellow-star':
                self.assertEqual(icon.get('y'), '32')
            elif icon.get('id') == 'yellow-star_hover':
                self.assertEqual(icon.get('y'), '64')
            else:
                self.fail('Invalid icon id: %s' % icon.get('id'))


class SVGPaddingTests(PyconizrTestCase):

    options = {'render': 'scss', 'padding': '2'}

    def test_padding_svg(self):

        # optimize first, so that we have clean SVG
        self.iconizr.optimize()
        self.iconizr.spritize()

        self.assertExists(self.iconizr.sprite.path)

        sprite_root = ET.parse(self.iconizr.temp_sprite).getroot()
        self.assertEqual(sprite_root.tag, self.nstag('svg'))
        self.assertEqual(sprite_root.get('width'), '32px')
        self.assertEqual(sprite_root.get('height'), '100px')
        self.assertEqual(sprite_root.get('viewBox'), '0 0 32 100')

        for icon in sprite_root:
            if icon.get('id') == 'red-triangle':
                self.assertEqual(icon.get('y'), '0')
            elif icon.get('id') == 'yellow-star':
                self.assertEqual(icon.get('y'), '34')
            elif icon.get('id') == 'yellow-star_hover':
                self.assertEqual(icon.get('y'), '68')
            else:
                self.fail('Invalid icon id: %s' % icon.get('id'))


class SVGHorizLayoutTests(PyconizrTestCase):

    options = {'render': 'scss', 'layout': 'horizontal'}

    def test_padding_svg(self):

        # optimize first, so that we have clean SVG
        self.iconizr.optimize()
        self.iconizr.spritize()

        self.assertExists(self.iconizr.sprite.path)

        sprite_root = ET.parse(self.iconizr.temp_sprite).getroot()
        self.assertEqual(sprite_root.tag, self.nstag('svg'))
        self.assertEqual(sprite_root.get('width'), '96px')
        self.assertEqual(sprite_root.get('height'), '32px')
        self.assertEqual(sprite_root.get('viewBox'), '0 0 96 32')

        for icon in sprite_root:
            if icon.get('id') == 'red-triangle':
                self.assertEqual(icon.get('x'), '0')
            elif icon.get('id') == 'yellow-star':
                self.assertEqual(icon.get('x'), '32')
            elif icon.get('id') == 'yellow-star_hover':
                self.assertEqual(icon.get('x'), '64')
            else:
                self.fail('Invalid icon id: %s' % icon.get('id'))


class SVGDiagLayoutTests(PyconizrTestCase):

    options = {'render': 'scss', 'layout': 'diagonal'}

    def test_padding_svg(self):

        # optimize first, so that we have clean SVG
        self.iconizr.optimize()
        self.iconizr.spritize()

        self.assertExists(self.iconizr.sprite.path)

        sprite_root = ET.parse(self.iconizr.temp_sprite).getroot()
        self.assertEqual(sprite_root.tag, self.nstag('svg'))
        self.assertEqual(sprite_root.get('width'), '96px')
        self.assertEqual(sprite_root.get('height'), '96px')
        self.assertEqual(sprite_root.get('viewBox'), '0 0 96 96')

        for icon in sprite_root:
            if icon.get('id') == 'red-triangle':
                self.assertEqual(icon.get('x'), '0')
                self.assertEqual(icon.get('y'), '0')
            elif icon.get('id') == 'yellow-star':
                self.assertEqual(icon.get('x'), '32')
                self.assertEqual(icon.get('y'), '32')
            elif icon.get('id') == 'yellow-star_hover':
                self.assertEqual(icon.get('x'), '64')
                self.assertEqual(icon.get('y'), '64')
            else:
                self.fail('Invalid icon id: %s' % icon.get('id'))

