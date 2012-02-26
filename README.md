Use gilt-python to access the Gilt API to obtain sale and product data on live and upcoming sales.

## Installation

Use [pip](http://www.pip-installer.org/en/latest/) to install:

    $ pip install gilt

You can fall back to ye olde way of installing (but pip is awesomer) by
[downloading the latest source (ZIP)](https://github.com/gilt/gilt-python/zipball/master "gilt-python
source code") and then run:

    $ python setup.py install

You may need to run the above commands with `sudo`.

## Getting Started

First register for a [developer API key](https://dev.gilt.com/user/register) and
[browse the API documentation](https://dev.gilt.com/page/gilt-public-apis).

### API Credentials

Access to the Gilt API needs an API key, which you can get for free. Once you have it,
it needs to be passed to the GiltRestClient constructor or passed as an environment variable:

```python
from gilt import GiltRestClient

apikey = "ACXXXXXXXXXXXXXXXXX"
client = GiltRestClient(apikey)
```

The better, more secure way is to set GILT_API_KEY in your environment, then construct your
client like:


```python

from gilt import GiltRestClient
client = GiltRestClient()
```

### Retrieve a list of all live sales

```python

from datetime import datetime
from gilt.rest import GiltRestClient
from gilt.util import sort_by_ending_soonest

client = GiltRestClient()
sales = client.sales.active.list()
sales.sort(sales, sort_by_ending_soonest)
now = datetime.now()
for sale in client.sales.active.list():
  print "%(name)s: %(description)s" % sale.__dict__
    if now > sale.begins: 
      print "  Begins in %s and finishes in %s" % (now - sale.begins, sale.ends - now)
    else: 
      print "  Began %s ago and finishes in %s" % (sale.begins - now, sale.ends - now)

```

### Retrieve upcoming sales in the womens store

```python

from gilt.rest import GiltRestClient

client = GiltRestClient()
sales = client.sales.upcoming.list('women')
for sale in client.sales.active.list():
  print "%s, %s: %d products" % (sale.name, sale.description, len(sale.products))

```

### Get details on a product in a sale

The below will print details on all products in the first active sale in the kids store.

```python

from gilt.rest import GiltRestClient

client = GiltRestClient()
sale = client.sales.active.list('kids')[0]
products = client.products.details.list(sale.products)
for i, product in enumerate(products):
  print "  %3d. %s by %s" % (, product.name, product.brand)
  for sku in product.skus
  print "     %s on sale for $%1.2f" % (sku.description, sku.sale_price)

```

## Design Principles

* Model classes should be pythonic.

  Users should not have to use dictionaries to access fields.
  Types should be what you expect, including dates.

* Loading data should be pythonic.

  Throwing together big and small programs should use familiar constructs with minimal magic.

* Respect and reflect the API

  Naming is kept as consistent as possible with exactly what the API provides.
  This includes methods, classes and fields.

* more...

