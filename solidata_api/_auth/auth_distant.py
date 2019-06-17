"""
auth_distant.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant ...")

import requests

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app, jsonify

def getDistantAuthUrl():
  auth_mode = app.config["AUTH_MODE"]
  log.debug("getDistantAuthUrl / auth_mode : %s", auth_mode )

  auth_url_root_modes = {
    "local" : app.config["AUTH_URL_ROOT_LOCAL"],
    "distant_prod" : app.config["AUTH_URL_ROOT_DISTANT_PROD"],
    "distant_preprod" : app.config["AUTH_URL_ROOT_DISTANT_PREPOD"],
  }

  auth_url_root = auth_url_root_modes[auth_mode]
  log.debug("getDistantAuthUrl / auth_url_root : %s", auth_url_root )

  return auth_url_root


def checkJWT(token, token_type, return_resp=False):
  """ 
  authenticate a token 
  sending request to the auth url / service 
  specified in config
  ... doing so to avoid middle man risk when editing
  """

  print (". "*50)

  auth_url_root = getDistantAuthUrl()
  log.debug("checkJWT / auth_url_root : %s", auth_url_root )






def distant_auth (func_name=None, as_decorator=True) : 
  """
  """
  log.debug("-@- distant_auth ...")
  log.debug("-@- distant_auth ... func_name : %s", func_name)
  computed = "test distannt_auth not as decorator"
  
  def _distant_auth(func):
    """
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
      
      print(".......")
      log.debug("-@- distant_auth ... inside")
      log.debug("-@- distant_auth ... inside ... func_name : %s", func_name)
      print(".......")

      ### DO STUFF 

      return func(*args, **kwargs)

    return wrapper

  if as_decorator : 
    return _distant_auth
  
  else : 
    return computed

