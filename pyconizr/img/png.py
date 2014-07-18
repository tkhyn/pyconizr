import os
import urllib

import cairo
import rsvg

from base import Image


class PNGfromSVG(Image):

    def __init__(self, svg, maxwidth=False, maxheight=False):

        png_path = os.path.splitext(svg.path)[0] + '.png'
        super(PNGfromSVG, self).__init__(png_path)

        self.svg = svg
        self.hdlr = rsvg.Handle(svg.path)

        self.maxw = maxwidth
        self.maxh = maxheight

        scale = 1

        w = _w = self.hdlr.props.width
        h = _h = self.hdlr.props.height

        if self.maxw and w > self.maxw:
            w = self.maxw
            scale = float(w) / float(_w)
            h = scale * _h
        if self.maxh and h > self.maxh:
            h = self.maxh
            scale = float(h) / float(_h)
            w = scale * _w

        self.width = w
        self.height = h
        self.scale = scale

        self.surf = None

    def data_type(self):
        return 'png;base64'

    def encoded_URI(self):
        return urllib.quote(open(self.path, 'rb').read().encode('base64'))

    def convert(self, force=True):

        if self.surf and not force:
            return

        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                       self.width, self.height)
        self.ctxt = cairo.Context(self.surf)
        self.ctxt.scale(self.scale, self.scale)

        self.hdlr.render_cairo(self.ctxt)
        # write_to_png requires a str (fails with a unicode arg)
        self.surf.write_to_png(str(self.path))
