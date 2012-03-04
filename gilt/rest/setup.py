import os
import logging
import iso8601
from datetime import datetime
import simplejson as json

# --- >8 --- >8 --- >8 --- >8 --- >8 --- >8

def rest_resource(klass):
  def nop(*args, **kwargs): pass
  
  #print "Restify: %s" % klass
  class_init = getattr(klass, '__init__', nop)
  fields = getattr(klass, 'fields', None) or dict()
  
  def __init__(self,  resource_client=None,  resource_base_url=None, resource_tail_url=None,  **kwargs):
    # Attributes startin with "resource_" are considered reserved names.
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
      #print "WARNING: class %s doesn't have field %s" %(klass.__name__, json_key)
      return json_value

  def load_json(json_blob, *args, **kwargs):
    if isinstance(json_blob, basestring):
      # The caller passed a plain old string, not a data structure (unless the
      # json a literal string, in which case you don't really need to load_json.)
      # Assume the intent is to parse the string first.
      json_blob = json.loads(json_blob)
    
    if isinstance(json_blob, dict):
      # The most common case is that a mapping of key/value pairs is received.
      # Transform each value into a strongly typed object first, keeping the key.
      # This transformed dictionary is then passed either to the class constructor
      # (which then assigns each (k,v) into self.k = v) or into a rest_key_assign'd
      # special loader function.
      transformed_json_dict = dict(
        (k, transform_json_value_type(k, v)) for k,v in json_blob.iteritems()
        )
      load_json_dict = getattr(klass, 'load_json_dict', None)
      if load_json_dict:
        return load_json_dict(transformed_json_dict)
      else:
        return klass(**transformed_json_dict)
      
    elif isinstance(json_blob, list):
      # Second most common case is to receive a list of things, like a list
      # of Sale or Product objects. This will decode each one and return as a list.
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

