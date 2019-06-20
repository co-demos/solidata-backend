"""
auth_distant_protocols.py  
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant_protocols ...")



functions_protocols = {

  ### DONE 
  "login_user" : {
    "endpoint_config" : "user_login",
    "endpoint_code" : "login",
  },

  ### DONE 
  "login_anonymous" : {
    "endpoint_config" : "user_login",
    "endpoint_code" : "login_anonymous",
  },

  ### DONE 
  "register_user" : {
    "endpoint_config" : "user_edit",
    "endpoint_code" : "register",
  },

  ### TO DO 
  "add_claims_to_access_token" : {
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "user_identity_lookup" : {
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "my_expired_token_callback" : {
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### WORKING ON IT
  "token_claims" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "token_claims",
  },
  
  ### WORKING ON IT
  # "anonymous_required" : {
  #   "endpoint_config" : "auth_tokens",
  #   "endpoint_code" : "token_claims",
  # },

  ### TO DO 
  # "anonymous_or_guest_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "guest_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "admin_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "staff_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "renew_pwd_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "reset_pwd_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "confirm_email_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  ### TO DO 
  # "current_user_required" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },
}