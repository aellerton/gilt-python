#!/usr/bin/env python

# TODO: make into proper unit tests
from gilt.rest.resources import json
from gilt.rest.resources import ProductLookImage


with open('tests/resources/sale-women-detail-fall-clearance.json') as src:
  json_content = json.load(src)
  json_image_urls = json_content['image_urls']
  json_300x184 = json_image_urls['300x184']
  print ">", json_300x184

  json_image = json_300x184[0]
  print ">>", json_image
  image = ProductLookImage.load_json(json_image)
  print ">>> Image:", image.__dict__
  assert image.width == 300
  assert image.height == 184
  assert image.url == 'http://cdn1.gilt.com/images/share/uploads/0000/0001/3924/139248813/orig.jpg'
  
  print "\n\n# Test image list..."
  image_list = ProductLookImage.load_json(json_300x184)

  print "  Number of images:", len(image_list)
  for image in image_list:
    print "    Image:", image
    print "      ", image.__dict__
    print

  
