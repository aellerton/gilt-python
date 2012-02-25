#!/usr/bin/env python
from mock import Mock, patch
from gilt.rest.resources import json
from gilt.rest.resources import Sale

parent = Mock()
parent.base_uri = ("https://api.twilio.com/2010-04-01/Accounts/"
   "AC123")
resource = Sale(parent, "PNd2ae06cced59a5733d2c1c1c69a83a28")

with open('tests/resources/sale-women-detail-fall-clearance.json') as f:
  entry = json.load(f)
  resource.load(entry)

  print resource
  for k,v in resource.__dict__.iteritems():
    print "%s: %s" % (k, v)

