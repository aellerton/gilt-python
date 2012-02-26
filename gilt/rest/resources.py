import re
from datetime import datetime
import logging
import httplib2
import iso8601

try: 
  import simplejson as json
except ImportError:
  try:
    import json
  except ImportError:
    from django.utils import simplejson as json

# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

def rest_resource(klass):
  def nop(*args, **kwargs): pass
  
  #print "Restify: %s" % klass
  class_init = getattr(klass, '__init__', nop)
  fields = getattr(klass, 'fields', None) or dict()
  
  def __init__(self, 
    resource_client=None, 
    resource_base_url=None,
    resource_tail_url=None, 
    **kwargs):
    self.resource_client = resource_client
    self.resource_base_url = resource_base_url
    self.resource_tail_url = resource_tail_url
    
    for k,v in kwargs.iteritems():
      setattr(self, k, v)
      
    # Invoke original constructor. TODO: This seems a bit unpythonic.
    class_init(self)
      
  def __repr__(self):
    return "%s(%s)" % ( self.__class__.__name__, ', '.join(
      ['%s=%r' % (k, v) for k, v in self.__dict__.iteritems() if not k.startswith('resource')]
      ))
    
  def transform_json_value_type(json_key, json_value):
    field_class = fields.get(json_key, None)
    if field_class:
      #print ">>field_class", json_key, field_class
      if hasattr(field_class, 'load_json'):
        return field_class.load_json(json_value)
      elif issubclass(field_class, basestring):
        # Strings are common. Avoid encoding issues and risk of duplicating
        # strings (not sure if it would) by just passing the string through.
        if isinstance(json_value, basestring):
          return json_value
        else:
          return field_class(json_value)
      elif issubclass(field_class, datetime):
        #print ">>> constructing '%s' -> %r as iso datetime" % (json_key, json_value)
        return iso8601.parse_date(json_value)
      else:
        #print ">>> constructing '%s' -> %r as %s" % (json_key, json_value, field_class)
        return field_class(json_value) # e.g. str, int, float
    else:
      return json_value

  def load_json(json_blob, *args, **kwargs):
    if isinstance(json_blob, basestring):
      # The caller passed a plain old string, not a data structure (unless the
      # json a literal string, in which case you don't really need to load_json.)
      # Assume the intent is to parse the string first.
      json_blob = json.loads(json_blob)
    
    if isinstance(json_blob, dict):
      transformed_json_dict = dict(
        (k,transform_json_value_type(k, v)) for k,v in json_blob.iteritems()
        )
      load_json_dict = getattr(klass, 'load_json_dict', None)
      if load_json_dict:
        return load_json_dict(transformed_json_dict)
      else:
        return klass(**transformed_json_dict)
      
    elif isinstance(json_blob, list):
      # The json_blob is a list of something kind of object. 
      return [load_json(sub_blob) for sub_blob in json_blob]
      
    else:
      raise TypeError("Don't know how to process %s" % type(json_blob))

  # Imbue the target class with our special methods.
  setattr(klass, '__init__', __init__)
  setattr(klass, '__repr__', __repr__)  
  setattr(klass, 'load_json', staticmethod(load_json))  
  return klass
  

def rest_key_assign(call, value_type):
  """Decorate a class with rest_key_assign to allow a member function
  to process the keys and values of a json dictionary directly.
  """
  def decorator_impl(klass):

    def load_json_dict(json_dict, *args, **kwargs):
      inst = klass()
      key_assign_method = getattr(inst, call)
      for json_key, json_blob in json_dict.iteritems():
        value = value_type.load_json(json_blob)
        key_assign_method(json_key, value)
      return inst
      
    setattr(klass, "load_json_dict", staticmethod(load_json_dict))
    return klass
  return decorator_impl

# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

@rest_resource
class ProductContent(object):
  pass


@rest_resource
class ProductLookImage(object):
  @property
  def size(self):
    """Convenience method to return (width,height) as a tuple.
    """
    return (self.width, self.height)


@rest_key_assign(call="add", value_type=ProductLookImage)
@rest_resource
class MediaSet(object):
  """xxx
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
    id = int,
    inventory_status = str, # TODO: consider a class here
    msrp_price = float,
    sale_price = float,
    attributes = SkuAttribute,
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
    content = ProductContent,
    image_urls = MediaSet,
    skus = Sku,
  )
    
  @property
  def num_skus(self):
    return len(self.skus)


@rest_resource
class Sale(object):
  """
  Retrieves a specific sale.

  details of a specific sale
    https://api.gilt.com/v1/sales/men/winter-weather-48/detail.json
  """
  fields = dict(
    name = str,
    sale = str, # api url for details
    sale_key = str,
    store = str,
    sale_url = str, # gilt.com url
    begins = datetime,
    ends = datetime,
    image_urls = MediaSet,
    description = str,
    products = None, # list of strings, each string is an api url for product details
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

