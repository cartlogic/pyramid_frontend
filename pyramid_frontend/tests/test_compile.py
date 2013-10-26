from __future__ import absolute_import, print_function, division

import os.path
import subprocess
from mock import patch
from unittest import TestCase
from cStringIO import StringIO

from .. import compile
from ..assets.compiler import Compiler
from ..assets.less import LessCompiler
from ..assets.requirejs import RequireJSCompiler

from . import utils
from .example import foo


class TestCompileCommand(TestCase):

    def test_pcompile_usage(self):
        args = [
            'pcompile',
        ]
        buf = StringIO()
        with patch('sys.stderr', buf):
            with self.assertRaises(SystemExit) as cm:
                compile.main(args)
            exit_exception = cm.exception
            self.assertEqual(exit_exception.code, 2)
        self.assertIn('config_uri', buf.getvalue())

    def test_pcompile(self):
        retcode = utils.compile_assets()
        self.assertEqual(retcode, 0)


class TestCompiler(TestCase):
    def setUp(self):
        self.theme = foo.FooTheme({})
        self.output_dir = os.path.join(utils.work_dir, 'compile-tests')

    def test_bad_shell(self):
        compiler = Compiler(None, '.')
        with self.assertRaises(subprocess.CalledProcessError):
            argv = [
                'false',
            ]
            compiler.run_command(argv)
            # XXX Try to test that this actually prints the stdout output of a
            # failed comamnd.

    def test_less_compile(self):
        compiler = LessCompiler(self.theme, self.output_dir)
        path = compiler.compile('main-less', '/_foo/css/main.less')
        f = open(path, 'rb')
        buf_minified = f.read()
        self.assertGreater(len(buf_minified), 0)

        # Test that minified version is smaller than non-minified.
        compiler = LessCompiler(self.theme, self.output_dir, minify=False)
        path = compiler.compile('main-less', '/_foo/css/main.less')
        f = open(path, 'rb')
        buf_unminified = f.read()

        self.assertLess(len(buf_minified), len(buf_unminified))

    def test_requirejs_compile(self):
        compiler = RequireJSCompiler(self.theme, self.output_dir)
        path = compiler.compile('main-js', '/_foo/js/main.js')
        f = open(path, 'rb')
        buf_minified = f.read()
        self.assertGreater(len(buf_minified), 0)

        # Test that minified version is smaller than non-minified.
        compiler = RequireJSCompiler(self.theme, self.output_dir, minify=False)
        path = compiler.compile('main-js', '/_foo/js/main.js')
        f = open(path, 'rb')
        buf_unminified = f.read()

        self.assertLess(len(buf_minified), len(buf_unminified))
