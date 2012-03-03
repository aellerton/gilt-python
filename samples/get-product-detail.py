#!/usr/bin/env python
from gilt.rest import GiltApiClient

# Get the first active sale in the womens store that has products
client = GiltApiClient()
for sale in client.sales.active('women'):
  product_urls = sale.products[0:3]
  if not product_urls: continue

  print 'First %d products (of %d) of sale "%s"' % (len(product_urls), len(sale.products), sale.name)
    
  for url in product_urls:
    product = client.products.get(url=url) 
    print
    print '  %s:' % product.name
    print '    Web:    %s' % product.url
    print '    Brand:  %s' % product.brand
    print '    Origin: %s' % product.content.origin
    print '    Images in %d resolution(s): %s'  % (
      len(product.image_urls), 
      ', '.join(["%s x %s" % (w,h) for (w,h) in product.image_urls.image_sizes])
      )
    for sku in product.skus:
      if 'color' in sku.attribute_names() and 'size' in sku.attribute_names():
        desc = 'Sku %s is %s size %s' % (sku.id, sku.attribute('color').value, sku.attribute('size').value)
      else:
        desc = 'Sku %s: %s' % (sku.id, ', '.join("%s=%s" % (k, sku.attribute(k).value) for k in sku.attribute_names()))
      print '      %-45s   Gilt: $%1.2f   MSRP $%1.2f' % (desc, sku.sale_price, sku.msrp_price)
      
  break # only do one sale

