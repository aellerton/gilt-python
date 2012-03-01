import os
import httplib2
import simplejson as json
from urllib import urlencode
from gilt import GiltException
from gilt import GiltRestException
from gilt import GiltAuthException
from gilt import AUTH_KEY_MISSING
from gilt.rest.resources import Sale
from gilt.rest.resources import SaleList
from gilt.rest.resources import Product


class GiltApiCredentials(object):
  def __init__(self, api_key=None):
    self.api_key = api_key or os.environ.get("GILT_API_KEY", None)
    
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


class GiltApiClient(object):
  """
  A client for accessing the Gilt REST API
  """
  def __init__(self, api_key=None, cred=None, base_url="https://api.gilt.com", version="v1", http=None):
    """
    Create a Gilt REST API client.
    """
    if cred is not None: self.cred = cred
    else: self.cred = GiltApiCredentials(api_key) # api_key==None means auto-detect.
    
    if not self.cred: raise GiltAuthException(AUTH_KEY_MISSING)

    self.base_url = '%s/%s' % (base_url, version)
    self.sales = SalesSection(self, self.base_url+'/sales')
    self.http = http or httplib2.Http
    self.products = Product(self, self.base_url+'/products')

  def get_json(self, url, params=None, cred=None, timeout=None):
    """Perform a GET request, parse the reply JSON.
    """
    if not url.endswith('.json'): url += '.json'
    
    if params is None: params = dict()
    if cred is None: cred = self.cred
    cred.install_parameters(params)
    url = '%s?%s' % (url, urlencode(params, doseq=True))
    
    headers = {}
    http = self.http(timeout=timeout)
    try:
      resp, content = http.request(url, 'GET', headers=headers, body=None)
      if int(resp.status) != 200:
        raise GiltRestException(resp.status, url, content)
      #print ">>>resp=",resp
      #print ">>>content len:",len(content)
      return json.loads(content)
    except json.decoder.JSONDecodeError, e:
      raise GiltException("Failed to load [%s]: %s" % (url, e), e)
    
    
class SalesSection(object):
  """
  Top level access to sales API calls.
  """
  def __init__(self, client, base_url):
    self.active = SaleList(client, base_url, '/active')
    self.upcoming = SaleList(client, base_url, '/upcoming')
    self.detail = Sale(client, base_url) # it will add {store}/{sale_key}/detail.json

