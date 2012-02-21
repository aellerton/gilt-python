import os
import logging

class GiltRestClient(object):
  """
  A client for accessing the Gilt REST API
  """
  def __init__(self, api_key=None, base_url="https://api.gilt.com", version="v1"):
    """
    Create a Gilt REST API client.
    """
    self.api_key = api_key or find_api_key()
    if not self.api_key:
      raise GiltAuthException("""
No apikey found either as a parameter or in the environment.
Specify it to the GiltRestClient constructor or as the environmen
variable ``GILT_API_KEY``.

Get keys from https://dev.gilt.com/user/register
""")

    base_url = '%s/%s' % (base_url, version)

    self.sales = Sales(base_url+'/sales', api_key)
    self.products = Products(base_url+'/products', api_key)


class SalesSection(object):
  """
  Top level access to sales API calls.
  """
  def __init__(self, base_url, api_key):
    self.active = Sales(base_url, api_key, '/active')
    self.upcoming = Sales(base_url, api_key, '/upcoming')
    self.details = Sale(base_url, api_key)


class Sales(ResourceList):
  """
  Retrieves lists of sales.

  all active sales:
    https://api.gilt.com/v1/sales/active.json

  all upcoming sales:
    https://api.gilt.com/v1/sales/upcoming.json

  all active sales in mens store
    https://api.gilt.com/v1/sales/men/active.json
  """
  def __init__(self, base_url, api_key, variant):
    self.base_url = base_url
    self.api_key = api_key
    self.variant = variant

  def list(self, store=None, **kwargs):
    """
    Returns a list of :class:`Sale` resources as a list. 

    :param store: If set, get sales only for this store (mens/womens/kids/home).
    """
    if store: 
      url = "%s/%s" % (self.base_url, self.variant)
    else:
      url = "%s/%s/%s" % (self.base_url, self.store, self.variant)
    return self.get_instances(params=params, url=url, **kwargs)

  
class Sale(Resource):
  """
  Retrieves a specific sale.

  details of a specific sale
    https://api.gilt.com/v1/sales/men/winter-weather-48/detail.json
  """
  def get(self, store=None, sale_key=None, uri=None):
    """
    Return details of a specific sale, identified either with store/sale_key pair
    or the uri.

    :param store: If set, specifies the store this sale belongs to. Must be set if sale_key is set.
    :param sale_key: If set, specifies the sale_key of interest. Must be set if store is set.
    :param uri: If set is a full or partial uri to the sale details.
    """
    if not uri: 
      if not store or not sale_url_key:
        raise GiltException("sale.get: If uri is not specified, set both store and sale_url_key")
      url = '%s/%s/%s/detail.json' % (self.base_url, store, sale_key)
    elif url.startswith('http'):
      # assuming url is absolute
      pass
    elif url.startswith('/'):
      url = "%s/%s" % (self.base_url, url.lstrip('/'))
    else:
      url = "%s/%s" % (self.base_url, url)

    return self.get_instance(url=url)
      

class Products(ResourceList):
  """
  Retrieves a lists of products.

  details of a specific product
    https://api.gilt.com/v1/products/124344157/detail.json
  """
  def __init__(self, base_url, api_key, variant):
    self.base_url = base_url
    self.api_key = api_key
    self.variant = variant

  def get(self, product_id_or_url, **kwargs):
    """
    Returns a single instance of :class:`Product`.

    :param product_id_or_url: either a product id or a url to retrieve.
    """
    if type(product_id_or_url) == types.IntType or \
      (type(product_id_or_url) == types.StringType and product_id_or_url.isdigit()):
      # caller has given a specific product id
      url = "%s/%s/detail" % (self.base_url, product_id_or_url)

    elif url.startswith('http'): # url is absolute
      pass

    else: # url is relative
      url = "%s/%s" % (self.base_url, url.lstrip('/'))

    return self.get_instance(url=url)

  def list(self, product_id_or_url_list, **kwargs):
    """
    Returns a list of :class:`Product` resources as a list. 

    :param product_id_or_url_list: each item in the list is either a product id or a url to retrieve.
    """
    
    if product_id_or_url_list in (types.StringType, types.IntType):
      # just in case the user passed a scalar
      return self.get(product_id_or_url_list, **kwargs)

    return [self.get(item) for item in product_id_or_url_list]
  
  
class Product(Resource):
  """
  Represents a specific product.

  details of a specific product
    https://api.gilt.com/v1/products/124344157/detail.json
  """
  pass

