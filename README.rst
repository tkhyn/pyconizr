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
   The input path containing the SVG files to generate the sprite from.
   Defaults to the current working directory.

out, -o
   The output path for the generated CSS/SASS/LESS file. The directory will be
   created if it does not already exist.
   Defaults to the current working directory.

out-sprite, -s
   The output path for the SVG and PNG sprites. The directory will be created
   if it does not already exist.
   Defaults to a 'sprite' directory in the current working directory.

out-fmt, -f
   The format to use for the CSS/SASS/LESS file. Must be a string equal to
   'css', 'sass' or 'less'.
   Defaults to 'css'.



.. |copyright| unicode:: 0xA9

.. _Iconizr: https://github.com/jkphl/iconizr
.. _grunt-iconizr: https://github.com/jkphl/grunt-iconizr
.. _scour: https://github.com/oberstet/scour
