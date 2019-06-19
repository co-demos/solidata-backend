"""
auth_distant_protocols.py  
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant_protocols ...")



functions_protocols = {

  ### DONE 
  "login_user" : {
    "auth_func" : "",
    "endpoint_config" : "user_login",
    "endpoint_code" : "login",
  },

  ### DONE 
  "login_anonymous" : {
    "auth_func" : "",
    "endpoint_config" : "user_login",
    "endpoint_code" : "login_anonymous",
  },

  ### DONE 
  "register_user" : {
    "auth_func" : "",
    "endpoint_config" : "user_edit",
    "endpoint_code" : "register",
  },

  ### TO DO 
  "add_claims_to_access_token" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "user_identity_lookup" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "my_expired_token_callback" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### WORKING ON IT
  "anonymous_required" : {
    "auth_func" : "",
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "token_claims",
  },

  ### TO DO 
  "anonymous_or_guest_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "guest_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "admin_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "staff_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "renew_pwd_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "reset_pwd_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "confirm_email_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },

  ### TO DO 
  "current_user_required" : {
    "auth_func" : "",
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
}