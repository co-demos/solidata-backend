"""
auth_distant.py  
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant ...")

import requests
import json

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app, jsonify

from . import functions_protocols





def getTokenFromRequest(api_request) : 
  """ 
  retrieve token sent with request 
  """ 

  log.debug("getTokenFromRequest ..." )
  # log.debug("getTokenFromRequest / api_request : \n%s", pformat(api_request.__dict__) )

  token_header_location = app.config["JWT_HEADER_NAME"]
  token_from_headers = api_request.headers.get(token_header_location, None)
  log.debug("getTokenFromRequest / token_from_headers : %s", token_from_headers )

  token_query_string = app.config["JWT_QUERY_STRING_NAME"]
  token_from_query = api_request.args.get(token_query_string, None)
  log.debug("getTokenFromRequest / token_from_query : %s", token_from_query )

  if token_from_headers or token_from_query : 
    return token_from_headers if token_from_headers else token_from_query
  else : 
    return None

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

def getDistantEndpointconfig (func_name) : 
  """ 
  """ 
  # print (". "*50)

  auth_dist_configs = app.config["AUTH_DISTANT_ENDPOINTS"]

  func_protocol = functions_protocols[func_name]
  field = func_protocol["endpoint_config"]
  subfield = func_protocol["endpoint_code"]
  endpoint_config = auth_dist_configs[field][subfield] 

  return endpoint_config

def distantAuthCall ( api_request=None, query={}, payload={}, func_name='user_login', url_var=None) :
  """ 
  sending request to the distant auth url / service 
  specified in config + env vars
  """

  print (". "*50)
  log.debug("distantAuthCall/ payload : \n%s", pformat(payload) )
  log.debug("distantAuthCall/ log_type : %s", func_name )
  log.debug("distantAuthCall/ url_var : %s", url_var )

  ### retrieve distant auth url root
  auth_url_root = getDistantAuthUrl()
  log.debug("distantAuthCall/ auth_url_root : %s", auth_url_root )

  ### retrieve distant auth endpoint config
  endpoint_config = getDistantEndpointconfig(func_name)
  log.debug("distantAuthCall/ endpoint_config : \n%s", pformat(endpoint_config) )
  
  url_append = endpoint_config["url"]
  post_args = endpoint_config["post_args"]
  url_args = endpoint_config["url_args"]
  method = endpoint_config["method"]
  resp_path = endpoint_config["resp_path"]



  ### TO DO : append url_append
  # get param from request



  ### build url base for specific auth
  base_url = auth_url_root + url_append 
  log.debug("distantAuthCall/ base_url : %s", base_url )

  

  ### append distant auth request headers
  headers = app.config["AUTH_URL_HEADERS"]
  if payload :
    headers = app.config["AUTH_URL_HEADERS_PAYLOAD"]

  ### TO DO : add token to requests in headers or query_string
  token = getTokenFromRequest(api_request)
  log.debug("token : %s", token )

  token_query_string = ""

  if token :
    token_locations = app.config["AUTH_URL_TOKEN_LOCATION"]
    
    if "query_string" in token_locations and  "headers" not in token_locations : 
      token_query_string_name = app.config["AUTH_URL_TOKEN_QUERY_STRING_NAME"]
      token_query_string = "{}={}".format(token_query_string_name,token)

    if "headers" in token_locations : 
      token_header_name = app.config["AUTH_URL_TOKEN_HEADER_NAME"]
      token_header_type = app.config["AUTH_URL_TOKEN_HEADER_TYPE"]
      headers[token_header_name] = token

  log.debug("distantAuthCall / headers : \n%s", pformat(headers) )




  ### TO DO : append url_args
  url_args_string = ""
  if url_args :
    url_args_string = "?"
    for arg_k, arg_v in url_args.items() : 
      url_args_string += "&{}={}".format( arg_k, query[arg_v]  )
  query_url = base_url + url_args_string + token_query_string



  ### send request to service and read response
  if method == 'GET' : 
    response = requests.get(query_url, headers=headers)

  elif method == 'DELETE' : 
    response = requests.delete(query_url, headers=headers)

  elif method in ['POST', 'PUT'] :

    ### TO DO : rebuild payload given 
    # remap payload given endpoint connfig 
    payload_remapped = {
      post_args[k] : v for k,v in payload.items() if k in post_args.keys()
    }
    log.debug("distantAuthCall / payload_remapped : \n%s", pformat(payload_remapped) )

    # then payload as json
    # payload_json = json.dumps(payload)
    payload_json = json.dumps(payload_remapped)
    log.debug("distantAuthCall / payload_json : %s", payload_json )

    if method == 'POST' : 
      response = requests.post(query_url, data=payload_json, headers=headers)

    elif method == 'PUT' : 
      response = requests.put(query_url, data=payload, headers=headers)


  log.debug("distantAuthCall / response.status_code : %s", response.status_code )
  response_json = response.json()
  log.debug("distantAuthCall / response_json : \n%s", pformat(response_json) )
  
  if resp_path : 
    ### remap response_json given resp_path if specific 
    response_json = { arg_k : response_json[arg_v] for arg_k, arg_v in resp_path.items() if arg_v in response_json.keys() }

  return response_json





def distant_auth( func_name=None, return_resp=True, ns_payload=False, raw_payload={}, url_var=None ) : 
  """
  """

  response = None

  log.debug("-@- distant_auth ...")
  log.debug("-@- distant_auth ... func_name : %s", func_name)
  
  is_distant_auth = app.config['AUTH_MODE'] == 'internal'
  log.debug("-@- distant_auth ... is_distant_auth : %s", is_distant_auth)

  def _distant_auth(func):
    """
    """

    log.debug("-@- distant_auth / before @wraps ... payload : \n%s", pformat(raw_payload))

    @wraps(func)
    def wrapper(*args, **kwargs):
      
      print(".......")
      log.debug("-@- distant_auth / inside")
      log.debug("-@- distant_auth / inside ... func_name : %s", func_name)
      log.debug("-@- distant_auth / inside ... return_resp : %s", return_resp)
      log.debug("-@- distant_auth / inside ... ns_payload : %s", ns_payload)
      log.debug("-@- distant_auth / inside ... raw_payload : \n%s", pformat(raw_payload))
      log.debug("-@- distant_auth / inside ... url_var : %s", url_var)
      
      payload = raw_payload

      if ns_payload :
        try :
          payload = request.get_json()
        except :
          payload = raw_payload

      log.debug("-@- distant_auth / inside ... payload : \n%s", pformat(payload) )

      if request : 
        log.debug("-@- distant_auth / there is a request ..." )
        # log.debug("getTokenFromRequest/ api_request : \n%s", pformat(request.__dict__) )
        response = distantAuthCall( api_request=request, func_name=func_name, payload=payload, url_var=url_var )
        log.debug("-@- distant_auth / inside ... response : \n%s", pformat(response))

      else : 
        log.debug("-@- distant_auth / there is no request ..." )
        # log.debug("getTokenFromRequest/ api_request : %s", pformat(request) )
        response = None

      print("... ... ...")

      if return_resp == False : 
        ### return decorated function if return_resp == True
        print("-@- distant_auth / return_resp == False / return function ....")
        return func(*args, **kwargs)
      
      else : 
        ### return result if return_resp == False 
        print("-@- distant_auth / return_resp == True / return response ....")
        return response

    return wrapper

  return _distant_auth
