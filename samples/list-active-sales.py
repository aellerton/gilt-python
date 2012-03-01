#!/usr/bin/env python
from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active():
  print "%s:" % sale.name
  print "  Store:    %s" % sale.store
  print "  Key:      %s" % sale.sale_key
  print "  Begins:   %s" % sale.begins
  print "  Visit:    %s" % sale.sale_url
  print "  For details:"
  print "    python samples/get-sale-detail.py %s %s" % (sale.store, sale.sale_key)
  print

