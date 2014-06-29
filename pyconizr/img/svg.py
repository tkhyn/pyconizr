import os
import re
from optparse import Values
from collections import defaultdict
import urllib
from copy import copy

from lxml import etree as ET, objectify
from scour import scour
import jinja2

from ..helpers import parseDim, f2str

from base import Image
from png import PNGfromSVG


# patch scour
scour.unwanted_ns.extend([
    'http://creativecommons.org/ns#',  # Creative Commons
    'http://purl.org/dc/elements/1.1/',  # DublinCore
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#',  # RDF
])


class SVGObj(Image):
    """
    Base class for SVG objects
    """

    def __init(self, path):
        super(SVGObj, self).__init__(path)
        self.xml = self.root = None
        self.png = None

    def save(self, iconizr):
        # default xml_declaration setting
        strip = iconizr.options['strip_xml_prolog']
        xml_dec = None if strip is None else not strip
        # write XML to file
        self.xml.write(self.path, xml_declaration=xml_dec)

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

    def makePNG(self):
        self.png = PNGfromSVG(self)
        self.png.convert()
        return True

    def data_type(self):
        return 'svg+xml'

    def encoded_URI(self):
        return urllib.quote(open(self.path, 'r').read().encode('utf-8'),
                            safe='~()*!.\'')


class SVGIcon(SVGObj):
    """
    An SVG icon that should be included in a SVGSprite
    """

    def __init__(self, path):
        super(SVGIcon, self).__init__(path)
        self.xml = ET.parse(self.path)
        self.root = self.xml.getroot()
        self.png = PNGfromSVG(self)

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

        # selector
        self.children = []
        self.selector = None

    def get_position(self):
        return (self.X, self.Y)

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

        self.dim_groups = defaultdict(lambda: [])

    def populate(self, iconizr):
        """
        Inserts all the SVGs in the sprite
        """
        ns_map = {}
        for icon in copy(self.icons):
            ns_map.update(icon.root.nsmap)
            self._add_icon(icon, iconizr)

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

    def _add_icon(self, icon, iconizr):

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

        # extract selector for compass spriting's magic selectors
        # http://compass-style.org/help/tutorials/spriting/magic-selectors/
        spl = icon.name.split('_')
        if len(spl) > 1:
            sel = spl[-1]
            if sel in iconizr.selectors:
                parent_name = '_'.join(spl[:-1])
                for i in self.icons:
                    if i.name == parent_name:
                        icon.selector = sel
                        i.children.append(icon)
                        self.icons.remove(icon)
                        return

        # check dimensions to see if it fits in an existing group
        self.dim_groups[(width, height)].append(icon)

    def makeOutput(self, iconizr):

        if not iconizr.render:
            return True

        if iconizr.render in ('css', 'scss'):
            # predefined output type, load built-in template
            templates_dir = os.path.join(os.path.dirname(__file__),
                                         '..', 'templates')
            template_name = 'sprite.' + iconizr.render
        else:
            templates_dir = os.path.dirname(iconizr.render)
            template_name = os.path.split(iconizr.render)[1]

        # create Jinja2 environment and load template
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
        template = env.get_template(template_name)

        # determine target outputs to generate
        dests = ['']  # default = svg sprite only

        if iconizr.options['png']:
            dests.append('png')

        if iconizr.options['data']:
            dests = ['-'.join((d, 'data')) for d in dests]

        out_icons = iconizr.options['out-icons']
        if out_icons:
            dests.extend(['-'.join((d, 'icons')) for d in dests])

        out_dir = os.path.join(iconizr.temp_dir, 'out')
        os.makedirs(out_dir)
        out_name = os.path.splitext(iconizr.out_name)[0]
        out_ext = os.path.splitext(iconizr.out_name)[1]
        if not out_ext:
            out_ext = os.path.splitext(template_name)[1]

        for dest in dests:
            # generate rendering context
            context = {
                'sprite': self,
                'common_class': iconizr.options['class'],
            }

            if 'icons' in dest:
                context['as_icons'] = True
                context['url_dir'] = iconizr.options['icons-url']
            else:
                context['url_dir'] = iconizr.options['sprites-url']

            if 'png' in dest:
                context['png'] = True

            if 'data' in dest:
                context['data'] = True

            # generate output file content
            out = template.render(context)

            # save file
            filename = ('-'.join((out_name, dest)) if dest else out_name) \
                     + out_ext
            out_file = open(os.path.join(out_dir, filename), 'w')
            out_file.write(out)
            out_file.close()
