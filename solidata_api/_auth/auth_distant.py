"""
auth_distant.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant ...")

import requests

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app, jsonify


functions_protocols = {
  "add_claims_to_access_token" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "user_identity_lookup" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "my_expired_token_callback" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "anonymous_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "anonymous_or_guest_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "guest_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "admin_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "staff_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "renew_pwd_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "reset_pwd_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "confirm_email_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "current_user_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
}


def getDistantAuthUrl():

  auth_mode = app.config["AUTH_MODE"]
  log.debug("getDistantAuthUrl / auth_mode : %s", auth_mode )

  if auth_mode != 'internal' : 

    auth_url_root_modes = {
      "local" : app.config["AUTH_URL_ROOT_LOCAL"],
      "distant_prod" : app.config["AUTH_URL_ROOT_DISTANT_PROD"],
      "distant_preprod" : app.config["AUTH_URL_ROOT_DISTANT_PREPOD"],
    }

    auth_url_root = auth_url_root_modes[auth_mode]
    # log.debug("getDistantAuthUrl / auth_url_root : %s", auth_url_root )

    return auth_url_root
  
  else :
    return False

def getDistantEndpoinntconfig (func_name) : 
  """ 
  """ 
  print (". "*50)

  auth_dist_configs = app.config["AUTH_DISTANT_ENDPOINTS"]
  func_protocol = functions_protocols[func_name]
  field = func_protocol["endpoint_config"]
  subfield = func_protocol["endpoint_code"]
  endpoint_config = auth_dist_configs[field][subfield] 

  return endpoint_config

def distantLoginRegister(payload, log_type='login', anonymous_token=None) :
  """ 
  login given a payload
  sending request to the auth url / service 
  specified in config
  ... doing so to avoid middle man risk when editing
  """

  print (". "*50)
  log.debug("distantLoginRegister / payload : %s", payload )
  log.debug("distantLoginRegister / log_type : %s", log_type )
  log.debug("distantLoginRegister / anonymous_token : %s", anonymous_token )

  auth_url_root = getDistantAuthUrl()
  log.debug("distantLoginRegister / auth_url_root : %s", auth_url_root )


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
  
  auth_url_root = getDistantAuthUrl()
  log.debug("-@- distant_auth / auth_url_root : %s", auth_url_root )

  def _distant_auth(func):
    """
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
      
      print(".......")
      log.debug("-@- distant_auth ... inside")
      log.debug("-@- distant_auth ... inside ... func_name : %s", func_name)
      print(".......")

      ### DO STUFF FOR DISTANT AUTH
      endpoint_config = getDistantEndpoinntconfig(func_name)
      log.debug("-@- distant_auth ... inside ... endpoint_config : \n%s", pformat(endpoint_config))





      return func(*args, **kwargs)

    return wrapper


  if as_decorator : 
    ### return decorated function if as_decorator == True
    return _distant_auth
  
  else : 
    ### return result if as_decorated == False 
    return computed

