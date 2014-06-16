"""
pyconizr
Python library to generate sprites from source SVG files
(c) 2014 Thomas Khyn
MIT license (see LICENSE.txt)
"""

from distutils.core import setup
import os

INC_PACKAGES = 'pyconizr',  # string or tuple of strings
EXC_PACKAGES = ()  # tuple of strings

install_requires = (
)

# imports __version__ variable
exec(open('pyconizr/version.py').read())
dev_status = __version_info__[3]

if dev_status == 'alpha' and not __version_info__[4]:
    dev_status = 'pre'

DEV_STATUS = {'pre': '2 - Pre-Alpha',
              'alpha': '3 - Alpha',
              'beta': '4 - Beta',
              'rc': '5 - Production/Stable',
              'final': '5 - Production/Stable'}

# setup function parameters
metadata = dict(
    name='pyconizr',
    version=__version__,
    description='Python library to generate sprites from source SVG files',
    author='Thomas Khyn',
    author_email='thomas@ksytek.com',
    url='http://bitbucket.org/tkhyn/pyconizr/',
    keywords=['iconizr', 'SVG', 'PNG', 'sprite'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Software Development :: Build Tools',
    ],
    scripts=['scripts/pyconizr.py']
)


# packages parsing from root packages, without importing sub-packages
root_path = os.path.dirname(__file__)
if isinstance(INC_PACKAGES, basestring):
    INC_PACKAGES = (INC_PACKAGES,)

packages = []
excludes = list(EXC_PACKAGES)
for pkg in INC_PACKAGES:
    pkg_root = os.path.join(root_path, *pkg.split('.'))
    for dirpath, dirs, files in os.walk(pkg_root):
        rel_path = os.path.relpath(dirpath, pkg_root)
        pkg_name = pkg
        if (rel_path != '.'):
            pkg_name += '.' + rel_path.replace(os.sep, '.')
        for x in excludes:
            if x in pkg_name:
                continue
        if '__init__.py' in files:
            packages.append(pkg_name)
        elif dirs:  # stops package parsing if no __init__.py file
            excludes.append(pkg_name)


def read(filename):
    return open(os.path.join(root_path, filename)).read()

setup(**dict(metadata,
   packages=packages,
   long_description=read('README.rst'),
   install_requires=install_requires
))
