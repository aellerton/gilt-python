#!/usr/bin/env python
import unittest
from gilt.rest.resources import json
from gilt.rest.resources import Product

class ProductTest(unittest.TestCase):

  def setUp(self):
    with open('tests/resources/product-detail-93603981.json') as src:
      self.json_content = json.load(src)

  def test_product_1(self):
    product = Product.load_json(self.json_content)
    self.assertEquals(product.name, 'Canvas Twill Timeless Trench')
    self.assertEquals(product.id, 93603981)
    self.assertEquals(product.brand, 'Gryphon')
    self.assertEquals(product.url, 'http://www.gilt.com/m/public/look/?utm_medium=api&utm_campaign=PublicAPIAlpha&utm_source=salesapi&s_id=4f9f381ffa13e06bf47b8e9994f1c8b87f58df34345d5ae1b213998dd627cb65_0_93603981')
    self.assertEquals(product.content.description, 'Cotton canvas twill blend woven trench coat. Snip.')
    self.assertEquals(product.content.material, '67% cotton and 33% nylon shell. 100% acetate lining')
    self.assertEquals(product.content.origin, 'China')
    print product.image_urls
    
    self.assertEquals(product.num_skus, 4)
    self.assertEquals(product.skus[0].id, 1225400)
    self.assertEquals(product.skus[0].inventory_status, 'for sale')
    self.assertEquals(product.skus[0].is_for_sale, True)
    self.assertEquals(product.skus[0].is_sold_out, False)
    self.assertEquals(product.skus[0].attribute('color').value, 'black')
    self.assertEquals(product.skus[0].attribute('hue').value, 'dark')
    
    self.assertEquals(product.skus[1].id, 1383500)
    self.assertEquals(product.skus[1].inventory_status, 'sold out')
    self.assertEquals(product.skus[1].is_for_sale, False)
    self.assertEquals(product.skus[1].is_sold_out, True)
    
    self.assertEquals(product.skus[3].id, 1383498)
    self.assertEquals(product.skus[3].attribute('color').value, 'red')
    #self.assertEquals(product.skus[3].attributes.color, 'red')
    
    
    #self.assertFalse(product.image_urls)
    
    
