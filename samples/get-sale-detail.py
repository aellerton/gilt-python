#!/usr/bin/env python
import sys
from gilt.rest import GiltApiClient
from gilt.util import print_sale_details

try:
  store = sys.argv.pop(1)
  sale_key = sys.argv.pop(1)
except IndexError:
  print "usage: python %s <store> <sale_key>" % sys.argv[0]
  print
  print "for examples, run:"
  print "  python samples/list-active-sales.py"
  print
  sys.exit(1)

sale = GiltApiClient().sales.detail(store, sale_key)
print_sale_details(sale)

