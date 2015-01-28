pyconizr
========

|copyright| 2014 Thomas Khyn

Python package to generate sprites from SVG icons

This package takes its inspiration from Iconizr_ and grunt-iconizr_ by
Joschi Kuphal.

From Joschi's words, Iconizr ...::

   ... takes a folder of SVG images and creates a CSS icon kit out of them.
   Depending on the client's capabilities, icons are served as SVG / PNG
   sprite or embedded data URIs. iconizr creates suitable CSS / Sass / LESS
   etc. resources and a JavaScript loader for easy integration into your
   HTML documents.

Not all the functionnalities from the original Iconizr are implemented yet,
but most of them are here.

Works on Python 2.6 and 2.7.


Installation
------------

As straighforward as it can be, using ``pip``::

   pip install pyconizr


Requirements
------------

Pyconizr will install all the required dependencies, except Cairo and librsvg
and their python bindings, which are needed to generate PNG images. Please make
sure they are installed in your environment if you want to use the pyconizr's
PNG functionalities.

If you are on Windows, the quickest way to install them is to use either PyGTK_
(for python 2.6 and 2.7) or PyGI_ (for python 2.7).



Usage
-----

From the command line::

   pyconizr [options]

From python::

   from pyconizr import iconize
   iconize(option1=val1, option2=val2, ...)


Default behavior
----------------

By default, pyconizr will:
   - optimize every SVG file in the current working directory using scour_
     (without overwriting them)
   - concatenate them to create an optimized SVG sprite in
     current_working_dir/sprites/sourcedir_name.svg
   - create a PNG sprite from the SVG sprite as
     current_working_dir/sprites/sourcedir_name.png
   - create a CSS/SCSS/whatever file at current_working_dir/sourcedir_name

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
     - css: for CSS output [default]
     - scss: for SASS output
     - no or ``Falsy`` from python: no output (to simply generate the sprite)
     - a path to a custom Jinja2_ template file for a 100% custom output (see
       existing templates for available variables)

static-url
   The absolute URL to the static directory. Used for links towards sprites and
   icons files from within the generated outputs.
   Defaults to ``/static``

sprites-url
   The absolute or relative (to static-url) URL to the sprites directory. Used
   for links towards sprite files.
   Defaults to ``sprites``

icons-url
   The absolute or relative (to static-url) URL to the icons directory. Used
   for links towards individual icons. Not used if out-icons is not defined.
   Defaults to ``icons``

padding
   Padding around the icons, in pixels.
   Defaults to ``0``.

layout
   The sprite layout. Can be vertical, horizontal or diagonal.
   Defaults to ``vertical``.

png/nopng
   By default, png fallbacks will be generated. When using the ``iconize``,
   function, use ``png=False`` to disable the behavior. With the command line,
   use ``--nopng``.
   Defaults to ``True``

data
   Should SVG and PNG images be linked as dataURIs? Remember that a page loads
   faster (thanks to caching vs dataURI decoding) if the CSS does not use
   dataURIs.
   Defaults to ``False``

class
   A common CSS class for all the icons in the sprite.
   Default to ``None``.

selectors
   Comma-separated list of selectors that can be embedded in icons filenames,
   using the ``_`` separator. For example, there a file name_hover.svg will be
   taken as the hovered version of the icon name.
   Defaults to ``hover,target,active``

unit
   The unit to be used for the ``background-position`` property. Only supposed
   to work with ``px`` and ``%``.
   Defaults to ``px``

scour-*
   All the options from scour_, using the 'scour-' prefix. For example,
   'strip-xml-prolog' becomes 'scour-strip-xml-prolog'.
   Defaults to best possible optimisation parameters for sprite generation.

   There are 2 command-line options added for scour parameters:

      scour-disable-comment-stripping

         Pyconizr enables comment stripping by default. When using the
         ``iconize`` function, use ``enable_comment_stripping=False`` to
         disable this feature. From the command line you need to use
         ``--scour-disable-comment-stripping``

      scour-verbose

         Pyconizr runs scour in quiet mode by default. If you need to see
         scour's non-error output, use ``quiet=False`` with the ``iconize``
         function, or ``--scour-verbose`` from the command line.


.. |copyright| unicode:: 0xA9

.. _Iconizr: https://github.com/jkphl/iconizr
.. _grunt-iconizr: https://github.com/jkphl/grunt-iconizr
.. _PyGTK: http://www.pygtk.org/downloads.html
.. _PyGI: http://sourceforge.net/projects/pygobjectwin32/
.. _scour: https://github.com/oberstet/scour
.. _Jinja2: http://jinja.pocoo.org
