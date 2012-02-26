import os
import logging
from urllib import urlencode
from gilt import GiltAuthException
from gilt.rest.resources import *

AUTH_KEY_MISSING = """
ERROR: API Key not set. 

The API key was not passed as a parameter nor set in the environment.
The recommended practice is to set the variable in your environment, e.g.

  $ export GILT_API_KEY='your-api-key-here'

Get keys from https://dev.gilt.com/user/register

You can also pass it to the GiltApiClient constructor.
"""

class GiltApiCredentials(object):
  def __init__(self, api_key=None):
    self.api_key = api_key or self.auto_detect()
    
  def __nonzero__(self):
    """This allows a Credentials object to be evaluated in a boolean context
    to determine if credentials are set or not. For example:
    
    if cred:
      print "looks set up ok"
    else:
      print "uh-oh, something isn't right"
    """
    return self.api_key is not None
    
  def install_parameters(self, request_params):
    """Modify request_params with apikey or whatever else is needed.
    
    :request_params: is a dict that will build to a query tring.
    """
    request_params['apikey'] = self.api_key
    
  @staticmethod
  def auto_detect():
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
  def __init__(self, api_key=None, cred=None, base_url="https://api.gilt.com", version="v1"):
    """
    Create a Gilt REST API client.
    """
    if cred is not None:
      self.cred = cred
    else:
      self.cred = GiltApiCredentials(api_key) # api_key==None means auto-detect.
      
    if not self.cred: raise GiltAuthException(AUTH_KEY_MISSING)

    base_url = '%s/%s' % (base_url, version)

    self.sales = SalesSection(self, base_url+'/sales')
    #self.products = Products(self, base_url+'/products')

  def get_json(self, url, params=None, cred=None):
    """Perform a GET request, parse the reply JSON.
    """
    if not url.endswith('.json'): url += '.json'
    
    if params is None: params = dict()
    if cred is None: cred = self.cred
    cred.install_parameters(params)
    #print "params"< params
    
    # TODO: encode params properly
    params = urlencode(params, doseq=True)
    url = '%s?%s' % (url, params)
    #print ">>url", url
    
    headers = {}
    method = 'GET'
    data = None
    timeout = None
    http = httplib2.Http(timeout=timeout)
    resp, content = http.request(url, method, headers=headers, body=data)
    
    #print ">>>resp=",resp
    #print ">>>content len:",len(content)
    return json.loads(content)
    
    
class SalesSection(object):
  """
  Top level access to sales API calls.
  """
  def __init__(self, client, base_url):
    self.active = SaleList(client, base_url, '/active')
    self.upcoming = SaleList(client, base_url, '/upcoming')
    self.detail = Sale(client, base_url) # it will add {store}/{sale_key}/detail.json

