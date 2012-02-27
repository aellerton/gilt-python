#!/usr/bin/env python
import sys
from gilt.rest import GiltApiClient
from gilt.util import print_sale_details

store = sys.argv.pop(1)
sale_key = sys.argv.pop(1)

sale = GiltApiClient().sales.detail(store, sale_key)
print_sale_details(sale)

