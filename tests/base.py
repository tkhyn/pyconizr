import os
import shutil
from copy import copy
from unittest import TestCase

from pyconizr.iconizr import Iconizr
from pyconizr.options import OPTIONS

__test__ = False
__unittest = True


class PyconizrTestCase(TestCase):
    """
    Create an Iconizr instance, and deletes the output directory at the end
    """

    options = {}

    # constant namespace prefix
    NS = '{http://www.w3.org/2000/svg}'

    def setUp(self):

        options = copy(self.options)
        for o, param in OPTIONS.iteritems():
            options.setdefault(param[1].get('dest', None) or o,
                               param[1]['default'])

        self.out_dir = os.path.join(os.path.dirname(__file__), 'out')
        options.update({'in': os.path.join(os.path.dirname(__file__), 'input',
                                           'icons'),
                        'out-path': self.out_dir,
                        'out-sprite': os.path.join(self.out_dir, 'sprites')})

        self.iconizr = Iconizr(**options)

    def tearDown(self):
        if os.path.exists(self.out_dir):
            shutil.rmtree(self.out_dir)
        self.iconizr.clean()

    def nstag(self, tag):
        """
        Transforms a simple tag into a namespaced tag
        """
        return self.NS + tag

    def assertExists(self, path, msg=None):
        if not os.path.exists(path):
            standardMsg = '%s does not exist' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertNotExists(self, path, msg=None):
        if os.path.exists(path):
            standardMsg = '%s exists' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsFile(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isfile(path):
            standardMsg = '%s is not a file' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertIsDir(self, path, msg=None):
        self.assertExists(path, msg)
        if not os.path.isdir(path):
            standardMsg = '%s is not a directory' % path
            self.fail(self._formatMessage(msg, standardMsg))

    def assertListDir(self, path, lst, msg=None):
        self.assertExists(path, msg)
        self.assertListEqual(os.listdir(path), lst)

    def assertSame(self, path1, path2, mode='b', msg=None):
        """
        Check that 2 files are identical
        """
        f1 = open(path1, 'r' + mode)
        f2 = open(path2, 'r' + mode)

        s1 = f1.read()
        s2 = f2.read()

        f1.close()
        f2.close()

        if mode == 't':
            # text mode
            self.assertEqual(s1, s2)
        elif not s1 == s2:
            self.fail(self._formatMessage(msg,
                                          'The files are binary different'))
