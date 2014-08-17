"""
pyconizr
Generate sprites from SVG icons
(c) 2014 Thomas Khyn
MIT license (see LICENSE.txt)
"""

from setuptools import setup, find_packages
import os
import sys


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

# calculate scour version depending on python version
if sys.version_info < (2, 7):
    scour_version = '<= 0.28'
else:
    scour_version = ''


# setup function parameters
setup(
    name='pyconizr',
    version=__version__,
    description='Generate sprites from SVG icons',
    long_description=open(os.path.join('README.rst')).read(),
    author='Thomas Khyn',
    author_email='thomas@ksytek.com',
    url='https://bitbucket.org/tkhyn/pyconizr/',
    keywords=['iconizr', 'SVG', 'PNG', 'sprite'],
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: %s' % DEV_STATUS[dev_status],
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Software Development :: Build Tools',
    ],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    package_data={
        '': ['LICENSE.txt', 'README.rst']
    },
    install_requires=(
        'scour%s' % scour_version,
        'lxml>=3.3',
        'jinja2>=2.7',
    ),
    entry_points={
        'console_scripts': [
            'pyconizr = pyconizr.run:execute_from_cl'
        ],
    }
)

try:
    import cairo
    try:
        import rsvg
    except ImportError:
        from gi.repository import Rsvg
except ImportError:
    import warnings
    warnings.warn("""
*********************************** WARNING ***********************************
 To use Pyconizr\'s PNG functionalities, you need to install cairo and rsvg as
 well as their Python bindings.
 On Windows, the easiest way to do it is to download and install the
 all-in-one version of PyGTK (python 2.6 and 2.7) or PyGI (python 2.7)
*******************************************************************************

""")
