"""
auth_distant_protocols.py  
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant_protocols ...")



functions_protocols = {

  ### DONE
  "token_claims" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "token_claims",
  },
  # TESTS TO DO  
  "confirm_access" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "confirm_access",
  },
  "new_access_token" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "new_access_token",
  },
  "fresh_access_token" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "fresh_access_token",
  },
  "new_refresh_token" : {
    "endpoint_config" : "auth_tokens",
    "endpoint_code" : "new_refresh_token",
  },


  ### DONE 
  "login_user" : {
    "endpoint_config" : "user_login",
    "endpoint_code" : "login",
  },
  "login_anonymous" : {
    "endpoint_config" : "user_login",
    "endpoint_code" : "login_anonymous",
  },


  ### DONE 
  "register_user" : {
    "endpoint_config" : "user_edit",
    "endpoint_code" : "register",
  },
  "confirm_email_user" : {
    "endpoint_config" : "user_edit",
    "endpoint_code" : "confirm_email",
  },
  "update_user" : {
    "endpoint_config" : "user_edit",
    "endpoint_code" : "user_update",
  },
  "delete_user" : {
    "endpoint_config" : "user_edit",
    "endpoint_code" : "user_delete",
  },

  ### TESTS TO DO  
  "password_forgotten" : {
    "endpoint_config" : "auth_password",
    "endpoint_code" : "pwd_forgot",
  },
  "password_reset_get" : {
    "endpoint_config" : "auth_password",
    "endpoint_code" : "pwd_reset_link",
  },
  "password_reset_post" : {
    "endpoint_config" : "auth_password",
    "endpoint_code" : "pwd_reset",
  },


  ### TESTS TO DO  
  "users_get_one" : {
    "endpoint_config" : "users_list",
    "endpoint_code" : "get_one",
  },
  "users_get_list" : {
    "endpoint_config" : "users_list",
    "endpoint_code" : "users_get_list",
  },







  # ### TO DO 
  # "add_claims_to_access_token" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  # ### TO DO 
  # "user_identity_lookup" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },

  # ### TO DO 
  # "my_expired_token_callback" : {
  #   "endpoint_config" : "users_list",
  #   "endpoint_code" : "get_one",
  # },



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