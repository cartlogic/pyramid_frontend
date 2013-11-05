from __future__ import absolute_import, print_function, division

from unittest import TestCase

from pyramid_frontend.theme import Theme


class TestTheme(TestCase):
    def test_traverse_attributes(self):
        class A(Theme):
            key = 'a'
            template_dir = 'a-templates'

        class B(A):
            key = 'b'
            pass

        class C(B):
            key = 'c'
            template_dir = 'c-templates'

        self.assertEqual(list(C.traverse_attributes('template_dir')),
                         [('c', 'c-templates'),
                          ('b', 'a-templates'),
                          ('a', 'a-templates')])

    def test_repr(self):
        class BlahTheme(Theme):
            key = 'blah'

        self.assertIn('blah', repr(BlahTheme(())))


class TestThemeOpt(TestCase):
    def setUp(self):
        class A(Theme):
            key = 'a'

        class B(Theme):
            key = 'b'
            frobozz = 127

        class C(Theme):
            key = 'c'
            frobozz = 42

        self.a = A({})
        self.b = B({})
        self.c = C({})

    def test_opt_missing(self):
        with self.assertRaises(AttributeError):
            self.a.opt('frobozz')

    def test_opt_missing_with_default(self):
        self.assertEqual(self.a.opt('frobozz', 'somedefault'), 'somedefault')

    def test_opt_present(self):
        self.assertEqual(self.b.opt('frobozz'), 127)

    def test_opt_override(self):
        self.assertEqual(self.c.opt('frobozz'), 42)
