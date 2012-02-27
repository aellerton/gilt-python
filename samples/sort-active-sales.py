#!/usr/bin/env python
from gilt.rest import GiltApiClient
from gilt.util import by_sale_name
from gilt.util import by_sale_begins

sales = GiltApiClient().sales.active()
stores = set(sale.store for sale in sales)
sales_per_store = [(store, sum(1 if sale.store==store else 0 for sale in sales)) for store in stores]

print "Retrieved all active sales"
print "  Total:       %d sales" % len(sales)
for count in sales_per_store:
  print "    %-9s  %d sales" % (count[0].title()+':', count[1])
print

print "First 5, in alphabetical order:"
sales.sort(by_sale_name)
for sale in sales[0:5]:
  print "  %-60s  Begins: %s" % (sale.name, sale.begins)
print

print "First 5, by begin time:"
sales.sort(by_sale_begins)
for sale in sales[0:5]:
  print "  %-60s  Begins: %s" % (sale.name, sale.begins)
print

