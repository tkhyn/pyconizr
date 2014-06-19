import os
import re
from optparse import Values
from collections import defaultdict

from lxml import etree as ET, objectify
from scour import scour
import jinja2

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
        self.name = os.path.splitext(os.path.split(path)[1])[0]

    def save(self, iconizr):

        # default xml_declaration setting
        strip = iconizr.options['strip_xml_prolog']
        xml_dec = None if strip is None else not strip
        # write XML to file
        self.xml.write(self.path, xml_declaration=xml_dec)

    def makePNG(self):
        self.png = PNGfromSVG(self.path)
        self.png.convert()


class SVGIcon(SVGObj):
    """
    An SVG icon that should be included in a SVGSprite
    """

    def __init__(self, path):
        super(SVGIcon, self).__init__(path)
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
                self.root.set(dim, f2str(getattr(self, dim), 'px'))

        # position initialisation
        self.X = self.Y = 0

    def optimize(self, iconizr):

        f = open(self.path, 'r')
        input_str = f.read()
        f.close()

        svg_opt = scour.scourString(input_str, Values(iconizr.options))

        # update XML tree
        self.root = ET.fromstring(svg_opt)
        self.xml._setroot(self.root)

        self.save(iconizr)

        return True

    def css_selector(self):
        return '.' + self.name

    def css(self, prop):
        if prop in ('height', 'width'):
            return f2str(getattr(self, prop), 'px')
        elif prop == 'background-position':
            return f2str(self.X, 'px') + ' ' + f2str(self.Y, 'px')
        else:
            raise ValueError('Invalid CSS property: ' + prop)


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

        self.dim_groups = defaultdict(lambda: [])

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

        # calculate position on the sprite
        width = icon.width
        height = icon.height

        icon.Y = self.height
        root_attrs = {'id': icon.name,
                      'y': f2str(icon.Y)}

        # change the sprite's offsets
        self.width = max(self.width, width)
        self.height += height

        for k, v in root_attrs.iteritems():
            icon.root.set(k, v)

        tag = icon.root.tag
        i = tag.find('}')
        if i >= 0:
            icon.root.tag = tag[i + 1:]

        self.root.append(icon.root)

        # check dimensions to see if it fits in an existing group
        self.dim_groups[(width, height)].append(icon)

    def makeOutput(self, iconizr):

        # destination file
        dest = os.path.join(iconizr.temp_dir, 'out', iconizr.out_name)
        os.makedirs(os.path.dirname(dest))

        # rendering context
        context = {
            'sprite': self,
            'common_class': iconizr.options['out-class'],
            'sprite_relpath':
                os.path.relpath(iconizr.tgt_sprite, iconizr.out_dir)
                       .replace('\\', '/')
        }

        # run templating engine
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                  os.path.join(os.path.dirname(__file__), 'templates')))

        template = env.get_template('sprite.' + iconizr.options['out-fmt'])
        out = template.render(context)

        out_file = open(dest, 'w')
        out_file.write(out)
        out_file.close()
