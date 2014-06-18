import os
import re
from optparse import Values

from lxml import etree as ET, objectify

from scour import scour

from helpers import parseDim, f2str
from png import PNGfromSVG


# patch scour
scour.unwanted_ns.extend([
    'http://creativecommons.org/ns#',  # Creative Commons
    'http://purl.org/dc/elements/1.1/',  # DublinCore
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#',  # RDF
])


class SVGObj(object):
    """
    Base class for SVG objects
    """

    def __init__(self, path):
        self.path = path
        self.id = os.path.splitext(os.path.split(path)[1])[0]

    def save(self, options={}):

        # default xml_declaration setting
        xml_dec = None if options['strip_xml_prolog'] is None \
                  else (not options['strip_xml_prolog'])
        # write XML to file
        self.xml.write(self.path, xml_declaration=xml_dec)


class SVGOpt(SVGObj):
    """
    An SVG file that should be optimized
    """

    def __init__(self, path):
        super(SVGOpt, self).__init__(path)
        self.xml = ET.parse(self.path)
        self.root = self.xml.getroot()
        self.png = PNGfromSVG(self.path)

        # extract dimensions
        for dim in ('width', 'height'):
            val = self.root.get(dim, False)
            if val:
                val = parseDim(val)

            setattr(self, dim, val)

        if not (self.width and self.height):
            # attempt to determine missing dimension(s)
            viewBox = self.root.get('viewBox', None)
            if viewBox:
                # with the viewBox attr
                viewBox = re.split('[^\d.]+', viewBox)
                for i in range(4):
                    try:
                        viewBox[i] = parseDim(viewBox[i])
                    except IndexError:
                        viewBox.append(0)
                    self.width = viewBox[2]
                    self.height = viewBox[3]

            if not (self.width and self.height):
                # with rendering
                self.width, self.height, __ = self.png.get_dimensions()

            for dim in ('width', 'height'):
                self.root.set(dim, f2str(getattr(self, dim)) + 'px')

    def optimize(self, options):

        f = open(self.path, 'r')
        input_str = f.read()
        f.close()

        svg_opt = scour.scourString(input_str, Values(options))

        # update XML tree
        self.root = ET.fromstring(svg_opt)
        self.xml._setroot(self.root)

        self.save(options)

        return True


class SVGSprite(SVGObj):
    """
    An SVG sprite made from SVGObj SVG objects
    """

    def __init__(self, path, icons):
        super(SVGSprite, self).__init__(path)

        self.icons = icons
        self.root = ET.Element('svg')
        self.xml = ET.ElementTree(self.root)
        self.width = self.height = 0

    def populate(self):
        """
        Inserts all the SVGs in the sprite
        """
        ns_map = {}
        for icon in self.icons:
            ns_map.update(icon.root.nsmap)
            self._add_icon(icon)

        # hack to make self.root inherit namespaces, as they would be erased
        # when self.root would be added to self.xml
        ns_def_root = ET.Element("nsdefroot", nsmap=ns_map)
        ns_def_root.append(self.root)
        # cleanup namespaces declarations to remove unneccessary ones
        objectify.deannotate(ns_def_root, cleanup_namespaces=True)

        # update the XML tree with the new dimensions
        w = f2str(self.width)
        h = f2str(self.height)
        attrs = {
            'width': w + 'px',
            'height': h + 'px',
            'viewBox': '0 0 %s %s' % (w, h)
        }
        for k, v in attrs.iteritems():
            self.root.set(k, v)

    def _add_icon(self, icon):

        # position on the sprite
        width = icon.width
        height = icon.height

        root_attrs = {'id': icon.id,
                      'y': f2str(self.height)}

        self.width = max(self.width, width)
        self.height += height

        for k, v in root_attrs.iteritems():
            icon.root.set(k, v)

        tag = icon.root.tag
        i = tag.find('}')
        if i >= 0:
            icon.root.tag = tag[i + 1:]

        self.root.append(icon.root)
