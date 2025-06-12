from django.test import SimpleTestCase
from app import calc


class ClacTests(SimpleTestCase):

    def test_add(self):
        res = calc.add(2, 2)
        self.assertEqual(res, 4)

    def test_subtract(self):
        res = calc.subtract(2, 2)
        self.assertEqual(res, 0)