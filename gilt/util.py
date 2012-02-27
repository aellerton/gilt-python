from textwrap import TextWrapper

def print_sale_details(sale):
  """Convenience method to print sale details to console.
  Nothing special here, just makes samples easier to read.
  """
  wrap = TextWrapper(initial_indent='  ', subsequent_indent='  ', width=80)
  
  print "Sale: \"%s\"" % sale.name
  print
  if sale.description: 
    print '\n'.join(wrap.wrap(sale.description))
    print
  print "  Begins:   %s" % sale.begins
  print "  Ends:     %s" % sale.ends
  print "  Duration: %s" % (sale.ends-sale.begins)
  print
  print "  Products:"
  if sale.products: 
    print "    %d products in this sale." % len(sale.products)
    for product in sale.products[0:3]:
      print "    %s" % product
    n = len(sale.products)-3
    if n>0:
      print "    ... %d more" % n
  else:
    print "    This sale has no products."
  print
  
  print "  Media set:"
  print "    %d resolution(s): %s" % (
    len(sale.image_urls), 
    ', '.join(["%s x %s" % (w,h) for (w,h) in sale.image_urls.image_sizes])
    )
  image_size = sale.image_urls.image_sizes[0]
  image_list = sale.image_urls.image_list(image_size)
  print "    %d x %d: %d image(s)" % (image_size[0], image_size[1], len(image_list))
  for image in image_list:
    print "      %s" % image.url
  
  print

def by_sale_name(a, b):
  return cmp(a.sale, b.sale)

def by_sale_begins(a, b):
  return cmp(a.begins, b.begins)

def by_sale_ends(a, b):
  return cmp(a.ends, b.ends)

