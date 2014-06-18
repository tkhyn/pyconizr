from lxml import etree as ET

from base import PyconizrTestCase


class SpritizeTests(PyconizrTestCase):

    options = {}

    def test_spritize_2_files(self):

        # optimize first, so that we have clean SVG
        self.iconizr.optimize()
        self.iconizr.spritize()

        self.assertExists(self.iconizr.temp_sprite)

        sprite_root = ET.parse(self.iconizr.temp_sprite).getroot()
        self.assertEqual(sprite_root.tag, self.nstag('svg'))
        self.assertEqual(sprite_root.get('width'), '32px')
        self.assertEqual(sprite_root.get('height'), '64px')
        self.assertEqual(sprite_root.get('viewBox'), '0 0 32 64')

        for icon in sprite_root:
            if icon.get('id') == 'red_triangle':
                self.assertEqual(icon.get('y'), '0')
            elif icon.get('id') == 'yellow_star':
                self.assertEqual(icon.get('y'), '32')
            else:
                self.fail('Invalid icon id: %s' % icon.get('id'))
