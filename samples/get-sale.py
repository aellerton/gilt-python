#!/usr/bin/env python
from mock import Mock
from gilt.rest.resources import json
from gilt.rest.resources import Sale

parent = Mock()
parent.base_uri = ("https://api.gilt.com/foo/bar/"
   "AC123")
resource = Sale(parent, "PNd2ae06cced59a5733d2c1c1c69a83a28")

with open('tests/resources/sale-women-detail-fall-clearance.json') as src:
  entry = json.load(src)
  resource.load(entry)

  print resource
  for k,v in resource.__dict__.iteritems():
    print "%s: %s" % (k, v)

