# gilt-python

Use gilt-python to access the Gilt API to obtain sale and product data on live and upcoming sales on gilt.com.

## 30-Second Guide

Do this:

    cd /wherever/you/want
    rm -f virtualenv.py && wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py playpython
    . ./playpython/bin/activate
    pip install gilt-python
    export GILT_API_KEY=xxxxxxxxxxxxxxxxxxx # get from https://dev.gilt.com/user/register
    python
    
    >>> from gilt.rest import GiltApiClient
    >>> for sale in GiltApiClient().sales.active(): # print the name of each active sale!
    ...   print sale.name
    ... 
    
    Calico Critters
    The Perfect Easter Outfit From Busy Bees
    Outdoor Style feat. Pearl River Modern…
    
    >>>

## Installation

The easiest installation is via pip:

    pip install gilt-python

You can clone the repo from github directly with:

    git clone git@github.com:aellerton/gilt-python.git
    cd gilt-python
    python setup.py install
    
You can also [download the latest source ZIP](https://github.com/gilt/gilt-python/zipball/master) or [tgz](https://github.com/aellerton/gilt-python/tarball/master) and unpack/install.

If you'd like to keep your python installation pristine and clean, ``virtualenv`` is your friend:

    cd /wherever/you/like
    rm -f virtualenv.py && wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py playpython
    . ./playpython/bin/activate

Now you should get this:

    (playpython) $ which python
    /wherever/you/like/playpython/bin/python

Installation is then as normal, and your "real" python installation will be untouched:

    cd gilt-python
    python setup.py install

You may need to run the install with `sudo`.

## Status

I've given the current release the version "0.7.1":

    >>> import gilt
    >>> gilt.__version__
    '0.7.1'

This is intended to convey "coming along, some weaknesses, but works". Hope that comes through ;)

Next scheduled work:

- change rest decorator to a subclass
- some general cleanups

## Getting Started

### API Credentials

The samples are written using the "auto-detect" API key model, which means you need to set
the API key in your environment, with:

    $ export GILT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxx

Get your API key for free at the [Gilt developer website](https://dev.gilt.com/user/register). [Browse the API documentation](https://dev.gilt.com/page/gilt-public-apis) while you're there. The gilt-python package reflects the Gilt API as much as it can, and attempts to be pythonic along the way.

When you set your API key this way you can instantiate a client with no arguments:

```python

from gilt.rest import GiltApiClient

client = GiltApiClient()
```

In your own programs you don't have to follow this approach. The client can be instantiated with an API key as a parameter, as below:

```python
from gilt.rest import GiltApiClient

client = GiltApiClient(api_key='xxxxxxxxxxxxxxxxxxxxxxx')
```

In general the environment variable method is encouraged.

### Try Sample Programs

If you are using the source distribution, you can run samples by first setting the ``PYTHONPATH`` variable:

    $ cd wherever/gilt-python
    $ export PYTHONPATH=`pwd`
    
You're all set up to run samples now. This one lists all active sales:

    $ python samples/list-active-sales.py 

    Fine Jewelry Personal Shopping:
      Store:    women
      Key:      fine-jewelry-concier
      For details:
        python samples/get-sale-detail.py women fine-jewelry-concier

The above program also shows how to use the ``get-sale-detail`` sample for any given sale, e.g.:

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

The next sample below prints details of the first 3 products in the first active sale:

    $ python samples/get-product-detail.py
    First 3 (of 132) products of sale "Amrita Singh Jewelry"

      Crystal Dune Necklace:
        Web:    http://www.gilt.com/m/public/look/?utm_medium=api&utm_campaign=PublicAPIAlpha&utm_source=salesapi&s_id=f9d44071e8cefa0dead8aa9a8da3d071cbfca617962e3aa764f98f105da94acc_0_139180171
        Brand:  Amrita Singh
        Origin: China
        Images in 3 resolution(s): 300 x 400, 91 x 121, 420 x 560
          Sku 1496513: color=crystal multi                Gilt: $78.00   MSRP $250.00

      ...

You can run unit tests with:

    $ nosetests tests/
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.082s
    
    OK
    

## Usage

### Print the name of all active (live) sales

```python

from gilt.rest import GiltApiClient

for sale in GiltApiClient().sales.active():
  print sale.name
```

The `Sales` object is not a python list, but it behaves like one.  You can sort the sales alphabetically like this:

```python

from gilt.rest import GiltApiClient
from gilt.util import by_sale_name

sales = GiltApiClient().sales.active()
sales.sort(by_sale_name)                  # <-- sort!
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

    women men kids home

For example:

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

