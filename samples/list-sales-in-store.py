#!/usr/bin/env python
from gilt.rest import GiltRestClient

client = GiltRestClient()
sales = client.sales.upcoming.list('women')
for sale in client.sales.active.list():
  print "%s, %s: %d products" % (sale.name, sale.description, len(sale.products))

