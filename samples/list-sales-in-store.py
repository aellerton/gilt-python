#!/usr/bin/env python
from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active.list('women'):
  print "%s: %d products" % (sale.name, len(sale.products))
  print "  %s" % sale.description
  print

# or:
# for sale in GiltApiClient().women.active.sales():
# ...
# ?

