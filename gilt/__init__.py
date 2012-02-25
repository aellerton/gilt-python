__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

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

