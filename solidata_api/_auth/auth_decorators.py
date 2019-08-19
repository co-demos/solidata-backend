# -*- encoding: utf-8 -*-

"""
auth_decorator.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_decorator ...")

from functools import wraps, partial, update_wrapper
from flask import request, current_app as app, jsonify

#### import extended JWT 
# cf : http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html
from solidata_api.application import jwt_manager
from flask_jwt_extended import (
  verify_jwt_in_request, verify_jwt_in_request_optional, create_access_token,
  get_jwt_claims, get_raw_jwt,
  jwt_optional, jwt_required
)

### import ext JWT check 
from .auth_distant import distantAuthCall, distant_auth # checkJWT


is_distant_auth = app.config['AUTH_MODE'] != 'internal'


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### AUTH DECORATORS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

"""
RESPONSE CODES 
cf : https://restfulapi.net/http-status-codes/

  200 (OK)
  201 (Created)
  202 (Accepted)
  204 (No Content)
  301 (Moved Permanently)
  302 (Found)
  303 (See Other)
  304 (Not Modified)
  307 (Temporary Redirect)
  400 (Bad Request)
  401 (Unauthorized)
  403 (Forbidden)
  404 (Not Found)
  405 (Method Not Allowed)
  406 (Not Acceptable)
  412 (Precondition Failed)
  415 (Unsupported Media Type)
  500 (Internal Server Error)
  501 (Not Implemented)


"""

### CLAIMS LOADER INTO JWT - for access_token
### cf : https://flask-jwt-extended.readthedocs.io/en/latest/custom_decorators.html 
@jwt_manager.user_claims_loader 
def add_claims_to_access_token(user):
  """
  Create a function that will be called whenever create_access_token
  is used. It will take whatever object is passed into the
  create_access_token method, and lets us define what custom claims
  should be added to the access token.

  > needs a 'model_user_out' or 'model_access' as 'user'
  """
  log.debug("-@- claims loader")
  log.debug("user : \n %s", pformat(user))

  # computed = distant_auth(func_name="add_claims_to_access_token", as_decorator=False)
  # log.debug("computed : %s", computed)

  sent_token = get_raw_jwt()
  log.debug("sent_token : \n %s", pformat(sent_token))

  ### common claims
  claims_to_store_into_jwt =  {
    '_id'					: user["_id"],
    'infos'				: user["infos"],
    'auth'				: user["auth"],
    'profile'			: user["profile"],
    # 'datasets'		: user["datasets"],
    # 'professional'	: user["professional"],
  }

  ### specific claims
  if "renew_pwd" in user : 
    claims_to_store_into_jwt["renew_pwd"] = user["renew_pwd"]

  if "reset_pwd" in user : 
    claims_to_store_into_jwt["reset_pwd"] = user["reset_pwd"]

  if "confirm_email" in user : 
    claims_to_store_into_jwt["confirm_email"] = user["confirm_email"]

  if user["infos"]["email"] == "anonymous" : 
    claims_to_store_into_jwt["is_anonymous"]  = True

  if "renew_refresh_token" in user : 
    claims_to_store_into_jwt["renew_refresh_token"] = True


  log.debug("claims_to_store_into_jwt : \n%s", pformat(claims_to_store_into_jwt))

  return claims_to_store_into_jwt


### IDENTITY LOADER - for access_token or refresh_token
### cf : http://flask-jwt-extended.readthedocs.io/en/latest/tokens_from_complex_object.html 
@jwt_manager.user_identity_loader
def user_identity_lookup(user):
  """
  Create a function that will be called whenever create_access_token
  is used. It will take whatever object is passed into the
  create_access_token method, and lets us define what the identity
  of the access token should be.
  """
  log.debug("-@- identity loader")
  log.debug("user : \n %s", pformat(user))
  
  # computed = distant_auth(func_name="user_identity_lookup", as_decorator=False)
  # log.debug("computed : %s", computed)

  try : 
    ### load email as identity in the jwt
    # identity = user["infos"]["email"]
    ### load _id as identity in the jwt
    # identity = str(user["_id"])
    identity = user["_id"]
  except : 
    identity = None
    
  log.debug("identity : \n %s", identity)

  return identity



### EXPIRED TOKENS
### cf : http://flask-jwt-extended.readthedocs.io/en/latest/changing_default_behavior.html 
@jwt_manager.expired_token_loader
def my_expired_token_callback():
  """
  Using the expired_token_loader decorator,
  we will now call this function whenever an expired
  token attempts to access an endpoint
  but otherwise valid access
  """

  log.debug("-@- expired token checker")

  ### if user is not confirmed, delete user from DB
  ### otherwise return a link to refresh refresh_token

  return jsonify({
    'msg'       : 'The token has expired',
    'status'    : 401,
    'sub_status': 42,
  }), 401



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### CUSTOM DECORATORS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
# cf : http://flask-jwt-extended.readthedocs.io/en/latest/custom_decorators.html 

def returnClaims(is_optional=False, return_anonymous_as_default=True):
  """
  """ 
  log.debug("-@- returnClaims / is_distant_auth : %s", is_distant_auth)

  anonymous_claims = {
    "_id" : None,
    "auth" : {
      "role" : None,
    },
    "renew_pwd" : False,
    "reset_pwd" : False,
    "confirm_email" : False,
  }

  if is_distant_auth : 
    ### distant call to get claims
    response = distantAuthCall( api_request=request, func_name="token_claims" )
    # log.debug("-@- returnClaims / response : \n%s", pformat(response) )
    if return_anonymous_as_default :
      claims = response.get( "claims", anonymous_claims )
    else :
      claims = response.get( "claims", {} )

  else : 

    log.debug("-@- returnClaims / local check / is_optional A : %s", is_optional)

    ### internal call to get claims
    # if is_optional == True :
    #   verify_jwt_in_request_optional()
    # else : 
    #   verify_jwt_in_request()

    log.debug("-@- returnClaims / local check / is_optional B : %s", is_optional)
    claims = get_jwt_claims()
    log.debug("-@- returnClaims / local check / claims A : \n%s", pformat(claims))
    if not claims and return_anonymous_as_default : 
      claims = anonymous_claims

  log.debug("-@- returnClaims / claims B : \n%s", pformat(claims) )

  return claims



def jwt_optional_sd(func):
  """
  Check if user has a valid jwt (optional)
  """

  log.debug("-@- jwt_optionnal_sd ...")

  @wraps(func)
  def wrapper(*args, **kwargs):

    ### 
    log.debug("kwargs : \n %s", pformat(kwargs) )
    claims = returnClaims(is_optional=True)
    log.debug("-@- jwt_optionnal_sd / claims : \n%s", pformat(claims))

    return func(*args, **kwargs)

  return wrapper


def jwt_required_sd(func):
  """
  Check if user has a valid jwt
  """

  log.debug("-@- jwt_required_sd ...")

  @wraps(func)
  def wrapper(*args, **kwargs):

    ### 
    log.debug("kwargs : \n %s", pformat(kwargs) )
    claims = returnClaims()
    log.debug("-@- jwt_required_sd / claims : \n%s", pformat(claims))
    
    return func(*args, **kwargs)

  return wrapper


def anonymous_required(func):
  """
  Check if user is not logged yet in access_token 
  and has a 'anonymous' role
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- anonymous required")

    ### ignore JWT / anonymous required if ANOJWT_MODE is disabled
    if app.config["ANOJWT_MODE"] == "no" : 
      return func(*args, **kwargs)
    
    ### otherwise verify jwt
    else :

      log.debug("kwargs : \n %s", pformat(kwargs) )
      # claims = returnClaims()

      if is_distant_auth : 
        log.debug("-@- anonymous required / is_distant_auth : %s", is_distant_auth)
        claims = returnClaims()
      #   response = distantAuthCall( request=request, func_name="anonymous_required" )
      #   log.debug("-@- anonymous checker / response : \n%s", pformat(response) )
      #   claims = response["claims"]

      else : 
        verify_jwt_in_request()
        claims = get_jwt_claims()
        log.debug("claims : \n %s", pformat(claims) )
        
      if claims["auth"]["role"] != 'anonymous' :
        return { "msg" : "Anonymous users only !!! You need to get an anonymous token" }, 403
      
      else :
        return func(*args, **kwargs)
  
  return wrapper


def anonymous_or_guest_required(func):
  """
  Check if user is not logged yet in access_token 
  and has a 'guest' or 'anonymous' role
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- anonymous_or_guest_required ")

    claims = returnClaims()

    if is_distant_auth : 
      log.debug("-@- anonymous_or_guest_required / is_distant_auth : %s", is_distant_auth)
      claims = returnClaims()
    #   response = distantAuthCall( request=request, func_name="token_claims" )
    #   log.debug("-@- anonymous checker / response : \n%s", pformat(response) )
    #   claims = response["claims"]

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()
      log.debug("-@- anonymous_or_guest_required / claims : \n %s", pformat(claims) )
    
    # log.debug("-@- anonymous_or_guest_required / kwargs : \n %s", pformat(kwargs) )

    if claims["auth"]["role"] not in ['guest', 'anonymous'] :
      return { "msg" : "Anonymous users or guests only !!! " }, 403
    else:
      return func(*args, **kwargs)
  
  return wrapper


def guest_required(func):
  """
  Check if user is not logged yet in access_token 
  and has a 'guest' or 'anonymous' role
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- guest_required")

    # claims = returnClaims()

    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()

    log.debug("-@- guest_required / claims : \n %s", pformat(claims) )
    
    # log.debug("-@- guest_required / kwargs : \n %s", pformat(kwargs) )

    if claims["auth"]["role"] not in  ['admin', 'guest', 'registred', "staff" ] :
      return { "msg" : "Registred users only !!! " }, 403
    else:
      return func(*args, **kwargs)
  
  return wrapper


def admin_required(func):
  """
  Check if user has admin level in access_token
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- admin_required")

    # claims = returnClaims()

    if is_distant_auth : 
      claims = returnClaims()
    
    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()

    log.debug("-@- admin_required / claims : \n %s", pformat(claims) )
    
    # log.debug("-@- admin_required / kwargs : \n %s", pformat(kwargs) )

    if claims["auth"]["role"] != 'admin':
      return { "msg" : "Admins only !!! " }, 403
    else:
      return func(*args, **kwargs)
  
  return wrapper


def staff_required(func):
  """
  Check if user has admin or staff level in access_token
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- staff_required")

    # claims = returnClaims()
  
    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()

    log.debug("-@- staff_required / claims : \n %s", pformat(claims) )
    
    # log.debug("-@- staff_required / kwargs : \n %s", pformat(kwargs) )

    if claims["auth"]["role"] not in  ['admin', 'staff']:
      return { "msg" : "Admins or staff only !!! " }, 403
    else:
      return func(*args, **kwargs)
  
  return wrapper


def renew_pwd_required(func):
  """
  Check if access_token has a claim 'renew_pwd' == True
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- renew_pwd checker")

    # claims = returnClaims()
  
    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()

    log.debug("-@- renew_pwd_required / claims : \n %s", pformat(claims) )
    
    # log.debug("-@- renew_pwd_required / kwargs : \n %s", pformat(kwargs) )

    try :
      if claims["renew_pwd"] == True:
        return func(*args, **kwargs)
    except :
      return { "msg" : "'renew_pwd' token expected !!! " }, 403
  
  return wrapper


def reset_pwd_required(func):
  """
  Check if access_token has a claim 'reset_pwd' == True
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- reset_pwd checker")

    log.debug("kwargs : \n %s", pformat(kwargs) )

    # claims = returnClaims()

    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()
    log.debug("-@- reset_pwd checker / claims : \n %s", pformat(claims) )

    try :  
      if claims["reset_pwd"] == True:
        return func(*args, **kwargs)
    except :
      return { "msg" : "'reset_pwd' token expected !!! " }, 403
  
  return wrapper


def confirm_email_required(func):
  """
  Check if access_token has a claim 'confirm_email' == True
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    
    log.debug("-@- confirm_email checker")
    # claims = returnClaims()

    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()

    log.debug("-@- confirm_email checker / claims : \n %s", pformat(claims) )
    
    if claims["confirm_email"] != True:
      return { "msg" : "'confirm_email' token expected !!! " }, 403
    else:
      return func(*args, **kwargs)
  
  return wrapper


### cf : https://stackoverflow.com/questions/13931633/how-can-a-flask-decorator-have-arguments/13932942#13932942
def current_user_required(func):
  """
  Check in access_token + user_oid if user eihter : 
  - is who he claims to be 
  - if he has admin level 
  """
  
  @wraps(func)
  def wrapper(*args, **kwargs):

    log.debug("-@- current_user_required")

    # claims = returnClaims()
  
    if is_distant_auth : 
      claims = returnClaims()

    else : 
      verify_jwt_in_request()
      claims = get_jwt_claims()
    log.debug("-@- current_user_required / claims : \n %s", pformat(claims) )

    # log.debug("-@- current_user_required / kwargs : \n %s", pformat(kwargs) )

    ### check in kwargs
    user_oid = kwargs["usr_id"] 
    log.debug( "user_oid : %s" , user_oid )
    
    ### check if oid sent is the same as the claim "_id"
    if user_oid != claims["_id"]  : 
      
      ### authorize if user is an admin
      if claims["auth"]["role"] == 'admin' :
        return func(*args, **kwargs)

      ### stops if user is neither an admin nor the current user
      else : 
        return { "msg" : "Admins or your own user only  !!! ".format(user_oid) }, 403

    else:
      return func(*args, **kwargs)
  
  return wrapper
