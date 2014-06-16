from base import PyconizrTestCase

from xml.etree import ElementTree as ET

NS = '{http://www.w3.org/2000/svg}'


class OptimizeTests(PyconizrTestCase):

    options = {}

    def test_optimize_individual_files(self):

        for svg_file in self.iconizr.svg_in:
            self.assertExists(svg_file.path)

        self.iconizr.optimize()

        for svg_file in self.iconizr.svg_in:
            svg_elt = ET.parse(svg_file.path + 'opt').getroot()
            self.assertEqual(svg_elt.tag, NS + 'svg')
            self.assertEqual(len(svg_elt), 1)

            g_elt = svg_elt[0]
            self.assertEqual(g_elt.tag, NS + 'g')
            self.assertEqual(len(g_elt), 1)

            path_elt = g_elt[0]
            self.assertEqual(path_elt.tag, NS + 'path')
            self.assertEqual(len(path_elt), 0)
