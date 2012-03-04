from datetime import datetime
from gilt.rest.setup import json
from gilt.rest.setup import rest_resource
from gilt.rest.setup import rest_key_assign


@rest_resource
class ProductContent(object):
  fields = dict(
    origin      = str,
    material    = str,
    description = str,
    )


@rest_resource
class ProductLookImage(object):
  fields = dict(
    url    = str,
    width  = int,
    height = int,
    )
  @property
  def size(self):
    """Convenience method to return (width,height) as a tuple.
    """
    return (self.width, self.height)


@rest_key_assign(call="add", value_type=ProductLookImage)
@rest_resource
class MediaSet(object):
  """A MediaSet represents a list of images in a set of resolutions.
  For example, there might be 3 images in 300x400 and 4 in 91x121.
  """
  def __init__(self):
    self.sets = dict()
    self.image_sizes = list()
    
  def __len__(self):
    return len(self.sets)/2
    
  def __contains__(self, key):
    return key in self.sets
    
  def add(self, key, image_list):
    width, height = key.split('x')
    size_tuple = (int(width), int(height))

    self.sets[key] = image_list
    assert size_tuple not in self.image_sizes # should never happen
    self.image_sizes.append(size_tuple)
    self.sets[size_tuple] = image_list

  def image_list(self, key):
    """Return the named image_list.
    
    :key: can be either the string size, like "300x184" or a tuple 
      (width, height).
    """
    return self.sets[key]


@rest_resource
class SkuAttribute(object):
  pass


@rest_resource
class Sku(object):
  fields = dict(
    id               = int,
    inventory_status = str, # TODO: consider a class here
    msrp_price       = float,
    sale_price       = float,
    attributes       = SkuAttribute,
  )
  
  def __init__(self):
    # properties are already loaded.
    self._attribute_index = dict((attribute.name, attribute) for attribute in self.attributes)

  def attribute(self, name):
    return self._attribute_index.get(name, None)

  def attribute_names(self):
    return self._attribute_index.keys()

  @property
  def is_for_sale(self):
    return getattr(self, 'inventory_status', None) == 'for sale'
  
  @property
  def is_sold_out(self):
    return getattr(self, 'inventory_status', None) == 'sold out'


@rest_resource
class Product(object):
  """
  Represents a specific product.

  details of a specific product
    https://api.gilt.com/v1/products/124344157/detail.json
  """
  fields = dict(
    id         = int, # TODO: consider rename to product_id, as id is technically reserved.
    name       = str,
    url        = str, # gilt.com url to view product. TODO: consider rename to gilt_url.
    product    = str, # Api Url to retrieve product details. TODO: consider rename to api_url.
    brand      = str,
    content    = ProductContent,
    image_urls = MediaSet,
    skus       = Sku,
  )
    
  @property
  def num_skus(self):
    return len(self.skus)

  def get(self, product_id=None, url=None):
    """Return a new Product object representing either product_id (if specified)
    or the full url. Either product_id or the url must be specified.
    """
    if product_id:
      # base_url is /products, so add {id}/detail.json
      url = '%s/%s/detail' % (self.resource_base_url, product_id)
    elif url:
      # nothing to do - the url must be ready to go.
      pass
    else:
      raise ValueError('Product.get: specify either product_id or url')
    
    return self.load_json(self.resource_client.get_json(url))
    
  @property
  def media_set(self):
    """This allows product.media_set to be an alias for product.image_urls.
    The name "image_urls" is how the API exposes the media set, but it may
    be more intutive to access it as "media_set".
    """
    return self.image_urls

  detail = get
  __call__ = get
  

@rest_resource
class Sale(object):
  """
  Retrieves a specific sale.

  details of a specific sale
    https://api.gilt.com/v1/sales/men/winter-weather-48/detail.json
  """
  fields        = dict(
    name        = str,
    sale        = str, # api url for details
    sale_key    = str,
    store       = str,
    sale_url    = str, # gilt.com url
    begins      = datetime,
    ends        = datetime,
    image_urls  = MediaSet,
    description = str,
    products    = None, # list of strings, each string is an api url for product details
    )
  
  def __init__(self):
    # some sales have no products, but that gets weird for code that expects
    # at least an empty list.
    if not hasattr(self, 'products'):
      self.products=[]
      
    # Same for descriptions
    if not hasattr(self, 'description'):
      self.description = ""
      
  @property
  def num_products(self):
    return len(self.products)
    
  def get(self, store, sale_key):
    # will add {store}/{sale_key}/detail.json
    url = '%s/%s/%s/detail' % (self.resource_base_url, store, sale_key)
    return self.load_json(self.resource_client.get_json(url))

  @property
  def media_set(self):
    """This allows sale.media_set to be an alias for sale.image_urls.
    The name "image_urls" is how the API exposes the media set, but it may
    be more intutive to access it as "media_set".
    """
    return self.image_urls
    
  detail = get
  __call__ = get
  

@rest_resource
class SaleList(object):
  """
  A list-like object representing a list of sales.
  Supports iteration and indexing by integer.

  all active sales:
    https://api.gilt.com/v1/sales/active.json

  all upcoming sales:
    https://api.gilt.com/v1/sales/upcoming.json

  all active sales in mens store
    https://api.gilt.com/v1/sales/men/active.json
  """
  fields = dict(
    sales = Sale # list of Sale objects
    )
  
  def __len__(self):
    return len(self.sales)
    
  def __iter__(self):
    return iter(self.sales)
    
  def __getitem__(self, index):
    return self.sales[index]

  def __setitem__(self, index, value):
    self.sales[index] = value

  def sort(self, by=None):
    self.sales.sort(by)
    
  def list(self, store=None):
    """
    Returns a list of :class:`Sale` resources as a list. 

    :param store: If set, get sales only for this store (mens/womens/kids/home).
    """
    if store: 
      store = '/%s' % store.lstrip('/')
    else:
      store = ''
      
    url = '%s%s%s' % (self.resource_base_url, store, self.resource_tail_url)
    return self.load_json(self.resource_client.get_json(url))

  __call__ = list

