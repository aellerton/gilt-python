#!/usr/bin/env python
from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active('women'):
  print "%s:" % sale.name
  if sale.description: print "  %s" % sale.description[0:80]
  if sale.products: print "  %d products" % len(sale.products)
  print "  Begins:   %s" % sale.begins
  print "  Ends:     %s" % sale.ends
  print "  Duration: %s" % (sale.ends-sale.begins)
  print

