from base import PyconizrTestCase

from lxml import etree as ET


class OptimizeTests(PyconizrTestCase):

    options = {}

    def test_optimize_individual_files(self):

        for icon in self.iconizr.icons:
            self.assertExists(icon.path)

        self.iconizr.optimize()

        for icon in self.iconizr.icons:
            icon_root = ET.parse(icon.path).getroot()
            self.assertEqual(icon_root.tag, self.nstag('svg'))
            self.assertEqual(len(icon_root), 1)

            g_elt = icon_root[0]
            self.assertEqual(g_elt.tag, self.nstag('g'))
            self.assertEqual(len(g_elt), 1)

            path_elt = g_elt[0]
            self.assertEqual(path_elt.tag, self.nstag('path'))
            self.assertEqual(len(path_elt), 0)
