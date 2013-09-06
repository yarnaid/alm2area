"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import alm2area.models as models


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class PixelMapTestCase(TestCase):

    def setUp(self):
        super().setUp()

    def test_pixel_map_lmax(self):
        pixel_map = models.gPixelMap()
        pixel_map.lmax = 7
        self.assertEquals(pixel_map.lmax, 7)
