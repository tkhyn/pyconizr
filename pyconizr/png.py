import os

import cairo
import rsvg


class PNGfromSVG(object):

    def __init__(self, svg_path, maxwidth=False, maxheight=False):
        self.path = svg_path
        self.hdlr = rsvg.Handle(svg_path)

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

        self.png = None

    def get_dimensions(self):
        return self.width, self.height

    def convert(self, dest=None, force=True):

        if self.png and not force:
            return

        if dest is None:
            dest = os.path.splitext(self.path)[0] + '.png'

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctxt = cairo.Context(surf)
        ctxt.scale(self.scale, self.scale)

        self.hdlr.render_cairo(ctxt)
        surf.write_to_png(dest)

        self.png = dest
