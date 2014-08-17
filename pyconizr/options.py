'''
Pyconizr options list
'''

import os
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from  six import iteritems

__all__ = ['OPTIONS']

_cwd = os.getcwd()

pyconizr_options = (
    ('in', (('-i',), dict(
        action='store',
        default=_cwd,
        help='Source files, as a directory or wildcard, can be a '
             'comma-separated list [default = cwd/*]'
    ))),
    ('out', (('-o',), dict(
        action='store',
        default=os.path.join(_cwd, 'out'),
        help='Output directory [default = cwd/out]'
    ))),
    ('out-sprite', (('-s',), dict(
        action='store',
        default=os.path.join(_cwd, 'sprites'),
        help='SVG and/or PNG sprite output directory or filename '
             '[default = out/sprites/auto_name.svg]'
    ))),
    ('out-icons', ((), dict(
        action='store',
        default=None,
        help='Individual SVG and PNG icons sub-directory, relative to '
             'the sprite output directory. If not specified, no individual '
             'icons are generated [default = None]'
    ))),
    ('render', (('-r',), dict(
        action='store',
        default='css',
        help='How the output should be rendered. Can be:\n'
             '- "css": for CSS output [default]\n'
             '- "scss": for SASS output\n'
             '- blank, "0", "False" or "None": no output (sprite only)\n'
             '- a path to a custom jinja2 template file'
    ))),
    ('static-url', ((), dict(
        action='store',
        default='/static',
        help='The absolute URL to the static directory [default = /static]'
    ))),
    ('sprites-url', ((), dict(
        action='store',
        default='sprites',
        help='The URL to the sprites directory, can be relative (to the '
             'static URL) or absolute [default = sprites]'
    ))),
    ('icons-url', ((), dict(
        action='store',
        default='icons',
        help='The URL to the icons directory, can be relative (to the '
             'static URL) or absolute. Has no effect if out-icons is '
             'not provided.'
             '[default = icons]. '
    ))),
    ('padding', ((), dict(
        action='store',
        default='0',
        help='Padding around the icons, in pixels. [default = 0]'
    ))),
    ('layout', ((), dict(
        action='store',
        choices=['none', 'vertical', 'horizontal', 'diagonal'],
        default='vertical',
        help='The sprite layout. Can be vertical, horizontal or diagonal. '
             '[default = vertical]'
    ))),
    ('png', (('-p',), dict(
        action='store_true',
        default=True,
        help='Generate PNG fallback sprite (or icons if out-icons is True) '
             '[default = True]'
    ))),
    ('data', (('-d',), dict(
        action='store_true',
        default=False,
        help='Do not generate any output file and generate data URIs instead '
             '[default = False]'
    ))),
    ('class', (('-c',), dict(
        action='store',
        default=None,
        help='A class name that is common to all icons [default = None]'
    ))),
    ('selectors', ((), dict(
        action='store',
        default='hover,target,active,',
        help='The selectors that can be embedded into filenames. '
             '[default = hover,target,active]'
    )))
)

OPTIONS = OrderedDict(pyconizr_options)


scour_options = (
    ('disable-simplify-colors', ((), dict(
        dest='simple_colors',
        action='store_false',
        default=True,
        help='won\'t convert all colors to #RRGGBB format'
    ))),
    ('disable-style-to-xml', ((), dict(
        dest='style_to_xml',
        action='store_false',
        default=True,
        help='won\'t convert styles into XML attributes'
    ))),
    ('disable-group-collapsing', ((), dict(
        dest='group_collapse',
        action='store_false',
        default=True,
        help='won\'t collapse <g> elements'
    ))),
    ('create-groups', ((), dict(
        dest='group_create',
        action='store_true',
        default=False,
        help='create <g> elements for runs of elements with identical '
             'attributes'
    ))),
    ('enable-id-stripping', ((), dict(
        dest='strip_ids',
        action='store_true',
        default=False,
        help='remove all un-referenced ID attributes'
    ))),
    ('enable-comment-stripping', ((), dict(
        dest='strip_comments',
        action='store_true',
        default=True,
        help='remove all <!-- --> comments'
    ))),
    ('shorten-ids', ((), dict(
        dest='shorten_ids',
        action='store_true',
        default=False,
        help='shorten all ID attributes to the least number of letters '
             'possible'
    ))),
    ('shorten-ids-prefix', ((), dict(
        dest='shorten_ids_prefix',
        action='store',
        default='',
        help='shorten all ID attributes with a custom prefix'
    ))),
    ('disable-embed-rasters', ((), dict(
        dest='embed_rasters',
        action='store_false',
        default=True,
        help='won\'t embed rasters as base64-encoded data'
    ))),
    ('keep-editor-data', ((), dict(
        dest='keep_editor_data',
        action='store_true',
        default=False,
        help='won\'t remove Inkscape, Sodipodi or Adobe Illustrator elements '
             'and attributes'
    ))),
    ('remove-metadata', ((), dict(
        dest='remove_metadata',
        action='store_true',
        default=True,
        help='remove <metadata> elements (which may contain license metadata '
             'etc.)'
    ))),
    ('renderer-workaround', ((), dict(
        dest='renderer_workaround',
        action='store_true',
        default=True,
        help='work around various renderer bugs (currently only librsvg) '
             '(default)'
    ))),
    ('no-renderer-workaround', ((), dict(
        dest='renderer_workaround',
        action='store_false',
        default=True,
        help='do not work around various renderer bugs (currently only '
             'librsvg)'
    ))),
    ('strip-xml-prolog', ((), dict(
        dest='strip_xml_prolog',
        action='store_true',
        default=None,
        help='won\'t output the <?xml ?> prolog'
    ))),
    ('enable-viewboxing', ((), dict(
        dest='enable_viewboxing',
        action='store_true',
        default=False,
        help='changes document width/height to 100%%/100%% and creates '
             'viewbox coordinates'
    ))),
    ('set-precision', ((), dict(
        dest='digits',
        action='store',
        type=int,
        default=5,
        help='set number of significant digits (default: 5)'
    ))),
    ('quiet', ((), dict(
        dest='quiet',
        action='store_true',
        default=True,
        help='suppress non-error output'
    ))),
    ('indent', ((), dict(
        dest='indent_type',
        action='store',
        default='none',
        help='indentation of the output: none, space, tab (default: none)'
    ))),
    ('protect-ids-noninkscape', ((), dict(
        dest='protect_ids_noninkscape',
        action='store_true',
        default=False,
        help='Don\'t change IDs not ending with a digit'
    ))),
    ('protect-ids-list', ((), dict(
        dest='protect_ids_list',
        action='store',
        default=None,
        help='Don\'t change IDs given in a comma-separated list'
    ))),
    ('protect-ids-prefix', ((), dict(
        dest='protect_ids_prefix',
        action='store',
        default=None,
        help='Don\'t change IDs starting with the given prefix'
    )))
)

SCOUR_OPTIONS = OrderedDict(scour_options)

# append scour options to the global options, with the 'scour-' prefix
for k, v in iteritems(SCOUR_OPTIONS):
    OPTIONS['scour-' + k] = v
