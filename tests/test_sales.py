#!/usr/bin/env python
import unittest
from gilt.rest.resources import json
from gilt.rest.resources import Sale
from gilt.rest.resources import SaleList

class SingleSaleTest(unittest.TestCase):

  def setUp(self):
    with open('tests/resources/sale-women-detail-fall-clearance.json') as src:
      self.json_content = json.load(src)

  def test_sale_1(self):
    sale = Sale.load_json(self.json_content)
    dur = sale.ends - sale.begins
    self.assertEquals(sale.name,        'Last Chance: Winter Apparel Up to 80% Off')
    self.assertEquals(sale.description, 'There\'s still time to pick up stylish wintertime staples before spring hits. Snip.')
    self.assertEquals(sale.sale_key,    'fall-clearance-bundl')
    self.assertEquals(sale.store,       'women')
    self.assertEquals(sale.sale_url,    'http://www.gilt.com/sale/women/fall-clearance-bundl?utm_medium=api&utm_campaign=PublicAPIAlpha&utm_source=salesapi')
    self.assertEquals(str(sale.begins), '2012-02-24 17:00:00+00:00') # 2012-02-24T17:00:00Z
    self.assertEquals(str(sale.ends),   '2012-02-26 05:00:00+00:00') # 2012-02-26T05:00:00Z
    self.assertEquals(str(dur),         '1 day, 12:00:00')
    
    self.assertEquals(len(sale.image_urls), 6)
    self.assertTrue((300,184) in sale.image_urls)
    self.assertTrue((300,280) in sale.image_urls)
    self.assertTrue((100,93) in sale.image_urls)
    self.assertTrue((636,400) in sale.image_urls)
    self.assertTrue((455,172) in sale.image_urls)
    self.assertTrue((370,345) in sale.image_urls)
    self.assertTrue('300x184' in sale.image_urls)
    self.assertTrue('300x280' in sale.image_urls)
    self.assertTrue('100x93' in sale.image_urls)
    self.assertTrue('636x400' in sale.image_urls)
    self.assertTrue('455x172' in sale.image_urls)
    self.assertTrue('370x345' in sale.image_urls)
    
    il = sale.image_urls.image_list('300x184')
    self.assertEquals(len(il), 2)
    self.assertEquals(il[0].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg')
    self.assertEquals(il[0].width, 300)
    self.assertEquals(il[0].height, 184)
    self.assertEquals(il[0].size, (300,184))
    self.assertEquals(il[1].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248815/orig.jpg')
    il = sale.image_urls.image_list('300x280')
    self.assertEquals(len(il), 1)
    il = sale.image_urls.image_list('100x93')
    self.assertEquals(len(il), 1)
    il = sale.image_urls.image_list('370x345')
    self.assertEquals(len(il), 1)

    self.assertEquals(len(sale.products), 231)
    self.assertEquals(sale.num_products, 231)

    self.assertEquals(sale.products[0], 'https://api.gilt.com/v1/products/93603981/detail.json')
    self.assertEquals(sale.products[1], 'https://api.gilt.com/v1/products/74107140/detail.json')
    self.assertEquals(sale.products[-2], 'https://api.gilt.com/v1/products/78754851/detail.json')
    self.assertEquals(sale.products[-1], 'https://api.gilt.com/v1/products/88513852/detail.json')


class ListSaleTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_active_1(self):
    with open('tests/resources/sales-active.json') as src:
      self.json_content = json.load(src)
      
    sales = SaleList.load_json(self.json_content)
    self.assertEquals(len(sales), 95)
    self.assertEquals(sales[0].name, 'Jewelry Under $50')
    self.assertEquals(sales[1].name, 'Watches Under $100')
    self.assertEquals(sales[-1].name, 'Fine Jewelry Personal Shopping')
    
    # prove iteration over all sales
    names = [sale.name for sale in sales]
    self.assertEquals(len(names), 95)
    self.assertEquals(names[0], 'Jewelry Under $50')
    self.assertEquals(names[1], 'Watches Under $100')
    self.assertEquals(names[-1], 'Fine Jewelry Personal Shopping')
    
  def test_upcoming_1(self):
    with open('tests/resources/sales-kids-upcoming.json') as src:
      self.json_content = json.load(src)
      
    sales = SaleList.load_json(self.json_content)
    self.assertEquals(len(sales), 35)
    self.assertEquals(sales[0].name, 'Peter Rabbit & Beatrix Potter')
    self.assertEquals(sales[1].name, 'Good Habit Gluten-Free')
    self.assertEquals(sales[-1].name, 'Wardrobe Essentials: Everything You Need')
    
    self.assertEquals(str(sales[0].begins), '2012-02-29 17:00:00+00:00') # 2012-02-29T17:00:00Z
    self.assertEquals(str(sales[0].ends),   '2012-03-05 17:00:00+00:00') # 2012-03-05T17:00:00Z
    self.assertEquals(sales[0].store, 'kids')

