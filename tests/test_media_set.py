#!/usr/bin/env python
import unittest
#from mock import Mock
#from gilt import GiltException
from gilt.rest.resources import MediaSet
#from gilt.rest.resources import ProductLookImage

MEDIA_SET_1 = """{
    "300x184": [
      {
        "url": "http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg",
        "width": 300,
        "height": 184
      },
      {
        "url": "http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248815/orig.jpg",
        "width": 300,
        "height": 184
      }
    ],
    "300x280": [
      {
        "url": "http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139249959/orig.jpg",
        "width": 300,
        "height": 280
      }
      ]}"""

class MediaSetTest(unittest.TestCase):

  def setUp(self):
    pass

  def test_media_set_1(self):
    ms = MediaSet.load_json(MEDIA_SET_1)
    print ms
    self.assertEquals(len(ms), 2)
    self.assertEquals(len(ms.image_sizes), 2)
    
    self.assertTrue((300,184) in ms.image_sizes )
    self.assertTrue((300,280) in ms.image_sizes)
    
    iml = ms.image_list('300x184')
    self.assertEquals(len(iml), 2)
    self.assertEquals(iml[0].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg')
    self.assertEquals(iml[0].width, 300)
    self.assertEquals(iml[0].height, 184)
    self.assertEquals(iml[1].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248815/orig.jpg')
    self.assertEquals(iml[1].width, 300)
    self.assertEquals(iml[1].height, 184)

    iml = ms.image_list((300,184))
    self.assertEquals(len(iml), 2)

    iml = ms.image_list('300x280')
    self.assertEquals(len(iml), 1)

    iml = ms.image_list((300,280))
    self.assertEquals(len(iml), 1)
    self.assertEquals(iml[0].url, 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139249959/orig.jpg')
    self.assertEquals(iml[0].width, 300)
    self.assertEquals(iml[0].height, 280)

