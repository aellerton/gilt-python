import os
import logging
#from gilt import GiltException
from gilt import GiltAuthException
from gilt.rest.resources import *

AUTH_KEY_MISSING = """
No apikey found either as a parameter or in the environment.
Specify it to the GiltRestClient constructor or as the environmen
variable ``GILT_API_KEY``.

Get keys from https://dev.gilt.com/user/register
"""

def detect_credentials():
  """
  Attempt to detect API key in the environment.
  """
  try:
    api_key = os.environ["GILT_API_KEY"]
    return api_key
  except KeyError:
    return None


class GiltApiClient(object):
  """
  A client for accessing the Gilt REST API
  """
  def __init__(self, api_key=None, base_url="https://api.gilt.com", version="v1"):
    """
    Create a Gilt REST API client.
    """
    self.api_key = api_key or detect_credentials()
    if not self.api_key:
      raise GiltAuthException(AUTH_KEY_MISSING)

    base_url = '%s/%s' % (base_url, version)

    self.sales = SalesSection(base_url+'/sales', api_key)
    self.products = Products(base_url+'/products', api_key)


