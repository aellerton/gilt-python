#!/usr/bin/env python
import unittest
from gilt.rest.resources import json
from gilt.rest.resources import Sku

class SkuTest(unittest.TestCase):

  def setUp(self):
    with open('tests/resources/product-detail-93603981.json') as src:
      self.json_content = json.load(src)

  def test_sku_1(self):
    self.assertTrue('skus' in self.json_content)
    json_skus = self.json_content['skus']
    self.assertEquals(len(json_skus), 4)
    json_sku = json_skus[0]
    self.assertTrue(isinstance(json_sku, dict))
    
    sku = Sku.load_json(json_sku)
    print sku
    self.assertEquals(sku.id, 1225400)
    self.assertEquals(sku.inventory_status, 'for sale')
    self.assertEquals(sku.is_for_sale, True)
    self.assertEquals(sku.msrp_price, 530.0)
    self.assertEquals(sku.sale_price, 99.0)
    
    self.assertEquals(len(sku.attributes), 2)
    self.assertEquals(len(sku._attribute_index), 2)
    self.assertTrue('color' in sku._attribute_index)
    attribute = sku.attribute('color')
    self.assertTrue(attribute is not None)
    self.assertEquals(attribute.name, 'color')
    self.assertEquals(attribute.value, 'black')
    attribute = sku.attribute('hue')
    self.assertEquals(attribute.name, 'hue')
    self.assertEquals(attribute.value, 'dark')
    
