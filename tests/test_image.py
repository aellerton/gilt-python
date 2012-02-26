#!/usr/bin/env python
import unittest
from mock import Mock
from gilt import GiltException
from gilt.rest.resources import ProductLookImage

SINGLE_1 = """{
        "url": "http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg",
        "width": 300,
        "height": 184
      }"""

SINGLE_2 = """{
        "url": "http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139249959/orig.jpg",
        "width": 300,
        "height": 280
      }"""

LIST_1 = "[%s, %s]" % ( SINGLE_1, SINGLE_2)
 
class ImageTest(unittest.TestCase):

  def setUp(self):
    pass
    #self.parent = Mock()
    #self.instance = AvailablePhoneNumber(self.parent)

  def test_single_1(self):
    im = ProductLookImage.load_json(SINGLE_1)
    self.assertEquals(im.url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg')
    self.assertEquals(im.width, 300)
    self.assertEquals(im.height, 184)

  def test_single_2(self):
    im = ProductLookImage.load_json(SINGLE_2)
    self.assertEquals(im.url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139249959/orig.jpg')
    self.assertEquals(im.width, 300)
    self.assertEquals(im.height, 280)

  def test_list_1(self):
    ims = ProductLookImage.load_json(LIST_1)
    self.assertEquals(len(ims), 2)
    self.assertEquals(ims[0].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg')
    self.assertEquals(ims[0].width, 300)
    self.assertEquals(ims[0].height, 184)
    self.assertEquals(ims[1].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139249959/orig.jpg')
    self.assertEquals(ims[1].width, 300)
    self.assertEquals(ims[1].height, 280)

