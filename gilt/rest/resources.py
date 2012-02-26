import re
from datetime import datetime
import logging

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

class RestInstanceResource(object):
  pass

class RestDictAssignable(object):
  pass

class DictMappable(object):
  pass

def RestInstanceResource2(klass):
  def nop(*args, **kwargs): pass
  
  print "Restify: %s" % klass
  class_init = getattr(klass, '__init__', nop)
  fields = getattr(klass, 'fields', None) or dict()
  
  def __init__(self, resource_url=None, resource_parent=None, resource_cred=None, **kwargs):
    print "rest init:"
    print "  kwargs:", kwargs
    
    # TODO: url, parent, cred
    for k,v in kwargs.iteritems():
      print "  set %s = %r" % (k, v)
      field = fields.get(k, None)
      if field:
        xx
      else:
        setattr(self, k, v)
    class_init(self)
      
  def load_json(json_blob, *args, **kwargs):
    print "load_json:", json_blob
    print "  args:", args
    print "  kwargs:", kwargs
    if isinstance(json_blob, dict):
      for k,v in json_blob.iteritems():
        print "  set %s = %r" % (k, v)
      return klass(**json_blob)
    elif isinstance(json_blob, list):
      return [load_json(sub_blob) for sub_blob in json_blob]
    else:
      raise TypeError("Don't know how to process %s" % type(json_blob))


  setattr(klass, '__init__', __init__)  
  setattr(klass, 'load_json', staticmethod(load_json))  
  return klass
  
# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8


class ProductContent(RestInstanceResource):
  pass

@RestInstanceResource2
class ProductImage(object):
  pass
  def __init__(self):
    print "original constructor"

class MediaSet(RestInstanceResource, RestDictAssignable):
  """xxx
  """
  @staticmethod
  def load_json_dict(json_dict):
    for key, part in json_dict.iteritems():
      self.add(key, ProductImage.load_json_list(part))
      
  
  def add(self, key, image_list):
    setattr(self, "size_"+key, iamge_list)


class SkuAttributes(InstanceResource, DictMappable):
  pass

class Sku(InstanceResource):
  fields = dict(
    msrp_price = float,
    sale_price = float,
    attributes = SkuAttributes,
  )
  

class Product(RestInstanceResource):
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


class SalesSection(object):
  """
  Top level access to sales API calls.
  """
  def __init__(self, base_url, api_key):
    self.active = Sales(base_url, api_key, '/active')
    self.upcoming = Sales(base_url, api_key, '/upcoming')
    self.details = Sale(base_url, api_key)


class Sales(ListResource):
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
    params = dict(apikey=self.api_key)
    return self.get_instances(params=params, url=url, **kwargs)

  
class Sale(RestInstanceResource):
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
      


class Products(ListResource):
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
  
  
