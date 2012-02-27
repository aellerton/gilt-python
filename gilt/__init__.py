__version_info__ = ('0', '7', '1')
__version__ = '.'.join(__version_info__)


AUTH_KEY_MISSING = """
ERROR: API Key not set. 

The API key was not passed as a parameter nor set in the environment.
The recommended practice is to set the variable in your environment, e.g.

  $ export GILT_API_KEY='your-api-key-here'

Get keys from https://dev.gilt.com/user/register

You can also pass it to the GiltApiClient constructor.
"""


class GiltException(Exception):
  pass

class GiltAuthException(Exception):
  pass

class GiltRestException(GiltException):
  def __init__(self, status, uri, msg=""):
    self.uri = uri
    self.status = status
    self.msg = msg

  def __str__(self):
    return "HTTP error %s: %s \n %s" % (self.status, self.msg, self.uri)


