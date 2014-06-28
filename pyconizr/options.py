'''
Pyconizr options list
'''

import os


__all__ = ['OPTIONS']

_cwd = os.getcwd()

OPTIONS = {
    'in': (('-i'), dict(
        action='store',
        default=_cwd,
        help='Source files, as a directory or wildcard, can be a '
             'comma-separated list [default = cwd/*]'
    )),
    'out': (('-o'), dict(
        action='store',
        default='css',
        help='The desired predefined output type, can be:\n'
             '- css: for CSS output [default]\n'
             '- scss: for SASS output\n'
             '- no: no output (to simply generate a sprite)\n'
             '- a path to a custom jinja2 template file'
    )),
    'out-path': (('-p'), dict(
        action='store',
        default=os.path.join(_cwd, 'out'),
        help='Output file name or directory [default = out]'
    )),
    'out-css-dir': ((), dict(
        action='store',
        default=None,
        help='The directory of the final CSS file if different from out-path '
             '[default = out-path]'
    )),
    'out-sprite': (('-s'), dict(
        action='store',
        default=os.path.join(_cwd, 'sprites'),
        help='SVG and/or PNG sprite output directory or filename '
             '[default = cwd/sprites/automatic_filename.svg]'
    )),
    'out-icons': ((), dict(
        action='store',
        choices=('no', 'also', 'only'),
        default='no',
        help='Should individual (optimised) icons be generated as well '
             '(also), instead of the sprite (only) or not at all (no)?'
             '[default = no]'
    )),
    'out-icons-dir': ((), dict(
        action='store',
        default='icons',
        help='Individual SVG and PNG icons sub-directory, relative to '
             'out-sprite [default = out-icons/icons]'
    )),
    'out-png': ((), dict(
        action='store_true',
        default=True,
        help='Generate PNG fallback sprite (or icons if out-icons is True) '
             '[default = True]'
    )),
    'out-data': ((), dict(
        action='store_true',
        default=False,
        help='Do not generate any output file and generate data URIs instead '
             '[default = False]'
    )),
    'out-class': (('-c'), dict(
        action='store',
        default=None,
        help='A class name that is common to all icons [default = None]'
    )),
}


SCOUR_OPTIONS = {
    'disable-simplify-colors': ((), dict(
        dest='simple_colors',
        action='store_false',
        default=True,
        help='won\'t convert all colors to #RRGGBB format'
    )),
    'disable-style-to-xml': ((), dict(
        dest='style_to_xml',
        action='store_false',
        default=True,
        help='won\'t convert styles into XML attributes'
    )),
    'disable-group-collapsing': ((), dict(
        dest='group_collapse',
        action='store_false',
        default=True,
        help='won\'t collapse <g> elements'
    )),
    'create-groups': ((), dict(
        dest='group_create',
        action='store_true',
        default=False,
        help='create <g> elements for runs of elements with identical '
             'attributes'
    )),
    'enable-id-stripping': ((), dict(
        dest='strip_ids',
        action='store_true',
        default=False,
        help='remove all un-referenced ID attributes'
    )),
    'enable-comment-stripping': ((), dict(
        dest='strip_comments',
        action='store_true',
        default=True,
        help='remove all <!-- --> comments'
    )),
    'shorten-ids': ((), dict(
        dest='shorten_ids',
        action='store_true',
        default=False,
        help='shorten all ID attributes to the least number of letters '
             'possible'
    )),
    'shorten-ids-prefix': ((), dict(
        dest='shorten_ids_prefix',
        action='store',
        type='string',
        default='',
        help='shorten all ID attributes with a custom prefix'
    )),
    'disable-embed-rasters': ((), dict(
        dest='embed_rasters',
        action='store_false',
        default=True,
        help='won\'t embed rasters as base64-encoded data'
    )),
    'keep-editor-data': ((), dict(
        dest='keep_editor_data',
        action='store_true',
        default=False,
        help='won\'t remove Inkscape, Sodipodi or Adobe Illustrator elements '
             'and attributes'
    )),
    'remove-metadata': ((), dict(
        dest='remove_metadata',
        action='store_true',
        default=True,
        help='remove <metadata> elements (which may contain license metadata '
             'etc.)'
    )),
    'renderer-workaround': ((), dict(
        dest='renderer_workaround',
        action='store_true',
        default=True,
        help='work around various renderer bugs (currently only librsvg) '
             '(default)'
    )),
    'no-renderer-workaround': ((), dict(
        dest='renderer_workaround',
        action='store_false',
        default=True,
        help='do not work around various renderer bugs (currently only '
             'librsvg)'
    )),
    'strip-xml-prolog': ((), dict(
        dest='strip_xml_prolog',
        action='store_true',
        default=None,
        help='won\'t output the <?xml ?> prolog'
    )),
    'enable-viewboxing': ((), dict(
        dest='enable_viewboxing',
        action='store_true',
        default=False,
        help='changes document width/height to 100%/100% and creates viewbox '
             'coordinates'
    )),
    'set-precision': ((), dict(
        dest='digits',
        action='store',
        type=int,
        default=5,
        help='set number of significant digits (default: 5)'
    )),
    'quiet': ((), dict(
        dest='quiet',
        action='store_true',
        default=True,
        help='suppress non-error output'
    )),
    'indent': ((), dict(
        dest='indent_type',
        action='store',
        type='string',
        default='none',
        help='indentation of the output: none, space, tab (default: none)'
    )),
    'protect-ids-noninkscape': ((), dict(
        dest='protect_ids_noninkscape',
        action='store_true',
        default=False,
        help='Don\'t change IDs not ending with a digit'
    )),
    'protect-ids-list': ((), dict(
        dest='protect_ids_list',
        action='store',
        type='string',
        default=None,
        help='Don\'t change IDs given in a comma-separated list'
    )),
    'protect-ids-prefix': ((), dict(
        dest='protect_ids_prefix',
        action='store',
        type='string',
        default=None,
        help='Don\'t change IDs starting with the given prefix'
    ))
}

for k, v in SCOUR_OPTIONS.iteritems():
    OPTIONS['scour-' + k] = v
