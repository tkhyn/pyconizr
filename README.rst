pyconizr
========

|copyright| 2014 Thomas Khyn

Python package to generate sprites from SVG files directories

This package is inspired from Iconizr_ and grunt-iconizr_ by Joschi Kuphal.

From Joschi's words, Iconizr ...::

   ... takes a folder of SVG images and creates a CSS icon kit out of them.
   Depending on the client's capabilities, icons are served as SVG / PNG
   sprite or embedded data URIs. iconizr creates suitable CSS / Sass / LESS
   etc. resources and a JavaScript loader for easy integration into your
   HTML documents.


Installation
------------

As straighforward as it can be, using ``pip``::

   pip install pyconizr


Usage
-----

From the command line::

   pyconizr.py [options]

From python::

   from pyconizr import iconize
   iconize(**options)


Default behavior
----------------

By default, pyconizr will:
   - optimize every SVG file in the current working directory using scour_
     (without overwriting them)
   - concatenate them to create an optimized SVG sprite in
     current_working_dir/sprites/sourcedir_name.svg
   - create a PNG sprite from the SVG sprite as
     current_working_dir/sprites/sourcedir_name.png
   - create a CSS/SCSS/LESS file at current_working_dir/sourcedir_name

This can be configured using the following options.

Options
-------

All options should be prefixed by ``--`` in the command line (if not using the
shortcut), or should be provided as keyword arguments to the ``iconize``
function.

in, -i
   The input directory or files (as a wildcard) that should be used to generate
   the sprite.
   Only valid SVG files will be taken into account, so there is no need to add
   a \*.svg wildcard ("dir/\*" will only include the \*.svg files in dir).
   Defaults to the current working directory.

out, -o
   The output path for the generated output file (CSS, SASS...). The directory
   will be created if it does not already exist.
   Defaults to the 'out' directory in the current working directory.

out-sprite, -s
   The output path for the SVG and PNG sprites. The directory will be created
   if it does not already exist.
   Defaults to the 'sprites' directory in the output directory.

out-icons
   The output path for the optimized SVG and rasterized PNG individual icons.
   If left blank, no icons will be generated. If defined, a supplementary
   output file will be generated with a '-icons' suffix.
   Defaults to blank (no icons generated).

render, -r
   How the output should be rendered. Can be:
     - css: for CSS output [default]\n'
     - scss: for SASS output\n'
     - no: no output (to simply generate a sprite)\n'
     - a path to a custom Jinja2_ template file for a 100% custom output

static-url
   The absolute URL to the static directory. Used for links towards sprites and
   icons files from within the generated outputs.
   Defaults to '/static'

sprites-url
   The absolute or relative (to static-url) URL to the sprites directory. Used
   for links towards sprite files.
   Defaults to 'sprites'

icons-url
   The absolute or relative (to static-url) URL to the icons directory. Used
   for links towards individual icons. Not used if out-icons is not defined.
   Defaults to 'icons'

class
   A common CSS class for all the icons in the sprite.
   Default to None.

png
   Should png fallbacks be generated?
   Defaults to True

data
   Should SVG and PNG images be linked as dataURIs? Remember that a page loads
   faster (thanks to caching vs dataURI decoding) if the CSS does not use
   dataURIs.
   Defaults to False

scour-*
   All the options from scour_, using the 'scour-' prefix. 'strip-xml-prolog'
   becomes 'scour-strip-xml-prolog'


.. |copyright| unicode:: 0xA9

.. _Iconizr: https://github.com/jkphl/iconizr
.. _grunt-iconizr: https://github.com/jkphl/grunt-iconizr
.. _scour: https://github.com/oberstet/scour
.. _Jinja2: http://jinja.pocoo.org
