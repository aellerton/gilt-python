import re
from datetime import datetime
import logging
import iso8601

try: 
  import simplejson as json
except ImportError:
  try:
    import json
  except ImportError:
    from django.utils import simplejson as json

import httplib2


# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8


class Resource(object):
    """A REST Resource"""

    name = "Resource"

    def __init__(self, base_uri, api_key):
        self.base_uri = base_uri
        self.api_key = api_key

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def request(self, method, uri, **kwargs):
        """
        Send an HTTP request to the resource.

        Raise a TwilioRestException
        """
        resp = make_twilio_request(method, uri, api_key=self.api_key, **kwargs)

        logging.debug(resp.content)

        if method == "DELETE":
            return resp, {}
        else:
            return resp, json.loads(resp.content)

    @property
    def uri(self):
        format = (self.base_uri, self.name)
        return "%s/%s" % format



# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

class InstanceResource(Resource):

    subresources = []
    id_key = "sid"

    def __init__(self, parent, sid):
        self.parent = parent
        self.name = sid
        super(InstanceResource, self).__init__(parent.uri,
            parent.api_key)

    def load(self, entries):
        if "from" in entries.keys():
            entries["from_"] = entries["from"]
            del entries["from"]

        if "uri" in entries.keys():
            del entries["uri"]

        self.__dict__.update(entries)

    def load_subresources(self):
        """
        Load all subresources
        """
        for resource in self.subresources:
            list_resource = resource(self.uri, self.parent.api_key)
            self.__dict__[list_resource.key] = list_resource

    def update_instance(self, **kwargs):
        a = self.parent.update(self.name, **kwargs)
        self.load(a.__dict__)

    def delete_instance(self):
        return self.parent.delete(self.name)



class ListResource(Resource):

    name = "Resources"
    instance = InstanceResource

    def __init__(self, *args, **kwargs):
        super(ListResource, self).__init__(*args, **kwargs)

        try:
            self.key
        except AttributeError:
            self.key = self.name.lower()

    def get(self, sid):
        """Return an instance resource """
        return self.get_instance(sid)

    def get_instance(self, sid):
        """Request the specified instance resource"""
        uri = "%s/%s" % (self.uri, sid)
        resp, item = self.request("GET", uri)
        return self.load_instance(item)

    def get_instances(self, params=None, page=None, page_size=None):
        """
        Query the list resource for a list of InstanceResources.

        Raises a TwilioRestException if requesting a page of results that does
        not exist.

        :param dict params: List of URL parameters to be included in request
        :param int page: The page of results to retrieve (most recent at 0)
        :param int page_size: The number of results to be returned.

        :returns: -- the list of resources
        """
        params = params or {}

        if page is not None:
            params["Page"] = page

        if page_size is not None:
            params["PageSize"] = page_size

        resp, page = self.request("GET", self.uri, params=params)

        if self.key not in page:
            raise TwilioException("Key %s not present in response" % self.key)

        return [self.load_instance(ir) for ir in page[self.key]]


    def load_instance(self, data):
        instance = self.instance(self, data[self.instance.id_key])
        instance.load(data)
        instance.load_subresources()
        return instance


# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8
# http://stackoverflow.com/questions/961048/get-class-that-defined-method-in-python
import inspect

def get_class_that_defined_method(meth):
  obj = meth.im_self
  for cls in inspect.getmro(meth.im_class):
    if meth.__name__ in cls.__dict__: return cls
  return None

# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

class RestInstanceResource(object):
  pass

class rest_dict_assignable(object):
  pass

class DictMappable(object):
  pass

def rest_instance_resource(klass):
  def nop(*args, **kwargs): pass
  
  #print "Restify: %s" % klass
  class_init = getattr(klass, '__init__', nop)
  fields = getattr(klass, 'fields', None) or dict()
  
  def __init__(self, resource_url=None, resource_parent=None, resource_cred=None, **kwargs):
    #print "rest init:"
    #print "  kwargs:", kwargs
    
    # TODO: url, parent, cred
    for k,v in kwargs.iteritems():
      #print "  set %s = %r" % (k, v)
      setattr(self, k, v)
      
    # Invoke original constructor. TODO: This seems a bit unpythonic.
    class_init(self)
      
  def __repr__(self):
    return "%s(%s)" % ( self.__class__.__name__, ', '.join(
      ['%s=%r' % (k, v) for k, v in self.__dict__.iteritems()]
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
      # assume caller passed raw text that needs to be parsed
      json_blob = json.loads(json_blob)
    #print "load_json:", json_blob
    #print "  args:", args
    #print "  kwargs:", kwargs
    
    if isinstance(json_blob, dict):
      transformed_json_dict = dict((k,transform_json_value_type(k, v)) for k,v in json_blob.iteritems())
      load_json_dict = getattr(klass, 'load_json_dict', None)
      if load_json_dict:
        return load_json_dict(transformed_json_dict)
      else:
        #for k,v in transformed_json_dict.iteritems():
        #  print "  set %s = %r" % (k, v)
        return klass(**transformed_json_dict)
    elif isinstance(json_blob, list):
      return [load_json(sub_blob) for sub_blob in json_blob]
    else:
      raise TypeError("Don't know how to process %s" % type(json_blob))

  setattr(klass, '__init__', __init__)
  setattr(klass, '__repr__', __repr__)  
  setattr(klass, 'load_json', staticmethod(load_json))  

  return klass
  
def rest_dict_assignable(value_type):
  def inner(method_to_wrap):
    #def invoke(*args, **kwargs):
    #  print ">>>invoke", args, kwargs
    #  
    #print "dict assign on %s" % method_to_wrap.__class__ #.imclass
    #print "inner!:", method_to_wrap
    method_to_wrap.__rest_dict_assign__=True
    #klass = get_class_that_defined_method(method_to_wrap)
    
    return method_to_wrap
  return inner

def rest_key_assign(call, value_type):
  def inner(klass):

    def load_json_dict(json_dict, *args, **kwargs):
      #print "hey, rest_dict_assign's load_json_dict"
      inst = klass()
      key_assign_method = getattr(inst, call)
      for json_key, json_blob in json_dict.iteritems():
        value = value_type.load_json(json_blob)
        key_assign_method(json_key, value)
      return inst
      
    setattr(klass, "load_json_dict", staticmethod(load_json_dict))
    return klass
  return inner

# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

@rest_instance_resource
class ProductContent(object):
  pass


@rest_instance_resource
class ProductLookImage(object):
  @property
  def size(self):
    """Convenience method to return (width,height) as a tuple.
    """
    return (self.width, self.height)
  


@rest_key_assign(call="add", value_type=ProductLookImage)
@rest_instance_resource
class MediaSet(object):
  """xxx
  """
  def __init__(self):
    self.sets = dict()
    self.image_sizes = set()
    
  def __len__(self):
    return len(self.sets)/2
    
  def __contains__(self, key):
    return key in self.sets
    
  def add(self, key, image_list):
    #print "in mediaset add:", key, image_list
    #setattr(self, "size_"+key, immge_list)
    width, height = key.split('x')
    size_tuple = (int(width), int(height))

    self.sets[key] = image_list
    self.image_sizes.add(size_tuple)
    self.sets[size_tuple] = image_list

  def image_list(self, key):
    """Return the named image_list.
    
    :key: can be either the string size, like "300x184" or a tuple 
      (width, height).
    """
    return self.sets[key]


#class SkuAttributes(InstanceResource, DictMappable):

@rest_instance_resource
class SkuAttribute(object):
  pass

@rest_instance_resource
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

@rest_instance_resource
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
  def num_image_lists(self):
    todo
    
  @property
  def num_skus(self):
    return len(self.skus)


class SalesSection(object):
  """
  Top level access to sales API calls.
  """
  def __init__(self, base_url, api_key):
    self.active = Sales(base_url, api_key, '/active')
    self.upcoming = Sales(base_url, api_key, '/upcoming')
    self.details = Sale(base_url, api_key)

  
@rest_instance_resource
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
  
  @property
  def num_products(self):
    return len(self.products)
  

@rest_instance_resource
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

