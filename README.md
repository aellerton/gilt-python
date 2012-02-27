Use gilt-python to access the Gilt API to obtain sale and product data on live and upcoming sales.

## Installation

Use [pip](http://www.pip-installer.org/en/latest/) to install:

    $ pip install gilt

You can fall back to ye olde way of installing (but pip is awesomer) by
[downloading the latest source (ZIP)](https://github.com/gilt/gilt-python/zipball/master "gilt-pythonsource code") and then run:

    $ python setup.py install

You may need to run the above commands with `sudo`.

## Getting Started

Before you run any sample you'll need an API key. These are free at the [Gilt developer website](https://dev.gilt.com/user/register). While there, [browse the API documentation](https://dev.gilt.com/page/gilt-public-apis).

### API Credentials

The samples are written using the "auto-detect" API key model, which means you need to set
the API key in your environment, with:

   $ export GILT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxx

Set up in this way you can instantiate a client with no arguments:

```python

from gilt import GiltRestClient

client = GiltRestClient()
```

In your own programs you don't have to follow this approach. The client can be instantiated with an API key as a parameter, as below:

```python
from gilt import GiltRestClient

client = GiltRestClient(api_key='xxxxxxxxxxxxxxxxxxxxxxx')
```

In general the environment variable method is encouraged.

### Running from source

If you are using the source distribution, you can run samples by first setting the ``PYTHONPATH`` variable:

    $ export PYTHONPATH=`pwd`
    $ python samples/list-active-sales.py 

    Fine Jewelry Personal Shopping:
      Store:    women
      Key:      fine-jewelry-concier
      For details:
        python samples/get-sale-detail.py women fine-jewelry-concier
    
    $ python samples/get-sale-detail.py women fine-jewelry-concier
    
    Sale: "Fine Jewelry Personal Shopping"
    
      Our Fine Jewelry Personal Shopping team is now available to offer one-on-one
      assistance in finding everything from classic investment pieces ...
    
      Begins:   2012-02-14 17:00:00+00:00
      Ends:     2012-02-28 17:00:00+00:00
      Duration: 14 days, 0:00:00
    
      Products:
        This sale has no products.
    
      Media set:
        6 resolution(s): 370 x 345, 300 x 280, 300 x 184, 455 x 172, 100 x 93, 636 x 400
        370 x 345: 1 image(s)
          http://cdn1.gilt.com/images/share/uploads/0000/0001/3802/138020020/orig.jpg

You can run unit tests with:

    $ nosetests tests/
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.082s
    
    OK
    

## Usage

### Retrieve a list of all active (live) sales

```python

from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active():
  print "%s:" % sale.name
```

The `Sales` object is not a python list, but it behaves like one.  You can sort the sales alphabetically like this:

```python

from gilt.rest import GiltApiClient
from gilt.util import by_sale_name

sales = GiltApiClient().sales.active()
sales.sort(by_sale_name)
for sale in sales:
  print sale.name
```

### Upcoming sales

Upcoming sales are retrieved with:

```python

from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.upcoming():
  print sale.name
```

### Picking a single store

The above examples get all gilt.com sales.

You can pick a single store by providing an argument to ``active()`` or ``upcoming()``. Current valid arguments are:

* women
* men
* kids
* home

```python

from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active('kids'):
  print "active kids sale: %s" % sale.name
```

Similarly, to retrive *upcoming* sales in the *womens* store:

```python

from gilt.rest import GiltRestClient

for sale in GiltApiClient().sales.upcoming('womens'):
  print "upcoming womens sale: %s" % sale.name
```

### Get details on a product in a sale

A ``Sale`` object contains URLs to retrieve details on the products for sale, but it does not directly contain the product details.

The example below will pick the first active sale in the kids store and then download and print details on the first 3 products:

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

* Timezone Neutral

  Everything is in UTC. It is recommended that you work with UTC except for display formatting.

* more...

