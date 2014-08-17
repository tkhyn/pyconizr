import os
import sys
import urllib

try:
    import cairo
except ImportError:
    cairo = None

try:
    import rsvg
except ImportError:
    if sys.platform == 'win32':
        try:
            from gi.repository import Rsvg as rsvg
        except:
            rsvg = None
    else:
        rsvg = None

from .base import Image


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

    def _check_libs(self):
        if not cairo:
            self.raise_lib_error('Cairo')
        if not rsvg:
            self.raise_lib_error('librsvg')

    def _raise_lib_error(self, lib):
        if sys.platform == 'win32':
            msg = ' On Windows, the recommended way to do that is to ' \
                'install PyGTK or PyGI, depending on your Python version.'
        else:
            msg = ''
        raise ImportError('%(Lib)s is necessary to use pyconizr\'s PNG '
            'functionalities, but could not be found or imported. Please '
            'make sure that %(lib)s and its Python bindings are installed.' %
            {'Lib': lib.capitalize(), 'lib': lib}
            + msg)

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
