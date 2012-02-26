#!/usr/bin/env python
import unittest
from gilt.rest.resources import ProductContent

PRODUCT_CONTENT_1 = """{
    "description": "Cotton canvas twill blend woven trench coat",
    "material": "67% cotton and 33% nylon shell. 100% acetate lining",
    "origin": "China"
  }"""

class ProductContentTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_content_1(self):
    pc = ProductContent.load_json(PRODUCT_CONTENT_1)
    self.assertEquals(pc.description, 'Cotton canvas twill blend woven trench coat')
    self.assertEquals(pc.material, '67% cotton and 33% nylon shell. 100% acetate lining')
    self.assertEquals(pc.origin, 'China')

