"""
config.py  
- settings for the flask application object
"""

import os
from datetime import timedelta

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

def formatEnvVar(var_name, format_type='boolean', separator=',', dict_separator=":") : 

  # print("formatEnvVar / var_name : ", var_name)

  env_var = os.getenv(var_name)
  # print("formatEnvVar / env_var : {} / var_name : {} ".format(env_var, var_name) )

  # if format_type in ['boolean', 'string'] :
  if format_type in ['boolean'] :
    if env_var in [ 'y', 'Y','yes', 'Yes', 'YES', 'true', 'True', 'TRUE', '1'] : 
      return True
    else :
      return False

  # print("...")  

  # trransform as none if it is the case
  if env_var in [ 'n', 'N', 'none', 'None', 'NONE', 'nan', 'Nan', 'NAN', 'null', 'Null','NULL', 'undefined'] : 
    env_var = None 
    if format_type == 'string' : 
      env_var = ""
    return env_var

  elif env_var and format_type == 'integer' : 
    return int(env_var)

  elif env_var and format_type == 'float' : 
    return float(env_var)

  elif env_var and format_type == 'list' : 
    return env_var.split(separator)

  elif env_var and format_type == 'dict' : 

    temp_list = env_var.split(separator)
    # print("formatEnvVar / temp_list : ", temp_list)
    env_dict = {}
    if len(temp_list) > 0 : 
      for tuple_dict in temp_list : 
        i = tuple_dict.split(dict_separator)
        env_dict[ i[0] ] = i[1] 
    return env_dict

  else : 
    return env_var

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# config_name    = os.getenv('FLASK_CONFIGURATION', 'default')
config_name    = os.getenv('RUN_MODE',     'default')
config_mongodb = os.getenv('MONGODB_MODE', 'local')
config_docker  = os.getenv('DOCKER_MODE',  'docker_off')
config_auth    = os.getenv('AUTH_MODE',    'internal')

print()
print("$ config_name : ",    config_name)  
print("$ config_mongodb : ", config_mongodb)  
print("$ config_docker : ",  config_docker) 


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### READ ENV VARS / MONGO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

MONGO_ROOT_LOCAL           = os.getenv('MONGO_ROOT_LOCAL') # "localhost"
MONGO_ROOT_DOCKER          = os.getenv('MONGO_ROOT_DOCKER') # "host.docker.internal"

MONGO_PORT_LOCAL           = os.getenv('MONGO_PORT_LOCAL') # "27017"

MONGO_ROOT_SERVER          = os.getenv('MONGO_ROOT_SERVER') # "127.0.0.1" # IP depending on your server's mongoDB configuration
MONGO_PORT_SERVER          = os.getenv('MONGO_PORT_SERVER') # "27017"
MONGO_USER_SERVER          = os.getenv('MONGO_USER_SERVER') # "MY-MONGODB-SERVER-ADMIN-USER"
MONGO_PASS_SERVER          = os.getenv('MONGO_PASS_SERVER') # "MY-SERVER-MONGODB-PASSWORD"
MONGO_OPTIONS_SERVER       = os.getenv('MONGO_OPTIONS_SERVER') # ""

MONGO_DISTANT_URI          = os.getenv('MONGO_DISTANT_URI') # "mongodb://<DISTANT-USERNAME>:<DISTANT-PASSWORD>@<DISTANT-HOST>:<DISTANT-PORT>"  
MONGO_DISTANT_URI_OPTIONS  = os.getenv('MONGO_DISTANT_URI_OPTIONS') # "?ssl=true&replicaSet=<REPLICA-SET>&authSource=admin&retryWrites=true"

# temporary dicts
mongodb_roots_dict = {
  "local"  : { 
    "docker_off" : MONGO_ROOT_LOCAL,  
    "docker_on"  : MONGO_ROOT_DOCKER  
  },
  "server" : { 
    "docker_off" : MONGO_ROOT_SERVER, 
    "docker_on"  : MONGO_ROOT_DOCKER  
  },
}

mongodb_ports_dict = {
  "local"  : MONGO_PORT_LOCAL,
  "server" : MONGO_PORT_SERVER,
}

mongodb_dbnames_dict = {
  "dev"       : os.getenv("MONGO_DBNAME",         "solidata"),
  "dev_email" : os.getenv("MONGO_DBNAME",         "solidata"),
  "preprod"   : os.getenv("MONGO_DBNAME_PREPROD", "solidata-preprod"),
  "prod"      : os.getenv("MONGO_DBNAME_PROD",    "solidata-prod")
}
### get DB name
mongodb_dbname = mongodb_dbnames_dict[config_name]

if config_mongodb == "distant" :
  mongodb_uri = "{}/{}{}".format(MONGO_DISTANT_URI, mongodb_dbname, MONGO_DISTANT_URI_OPTIONS)

else : 
  mongodb_root = mongodb_roots_dict[config_mongodb][config_docker]
  mongodb_port = mongodb_ports_dict[config_mongodb]

  ### get login if mongodb hosted on a server
  mongodb_login = "" 
  mongodb_options = "" 
  if config_name == "server" : 
    mongodb_login = "{}:{}@".format(MONGO_USER_SERVER, MONGO_PASS_SERVER)
    mongodb_options = MONGO_OPTIONS_SERVER ### must begin with "?"

  mongodb_uri = "mongodb://{}{}:{}/{}{}".format(mongodb_login, mongodb_root, mongodb_port, mongodb_dbname, mongodb_options)

print(" --- MONGODB_URI : ", mongodb_uri) 
os.environ["MONGODB_URI"] = mongodb_uri 


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###





class BaseConfig(object):  

  # CODE_LINK = "<a target='_blank' href='https://github.com/entrepreneur-interet-general/solidata_backend'>Solidata_backend</a>"
  CODE_LINK = "<a target='_blank' href='"+os.getenv('CODE_URL')+"'>Solidata_backend</a>"
  CODE_URL = os.getenv('CODE_URL')

  # APP VERSION 
  APP_VERSION = os.getenv('APP_VERSION') 
  
  # RUN_MODE          = "dev"
  RUN_MODE  = os.getenv("RUN_MODE")

  # DEBUG              = True
  DEBUG = formatEnvVar('DEBUG', format_type='boolean') # True

  """ HOST """
  SERVER_NAME_TEST  = "True" 
  # SERVER_NAME =  os.getenv("SERVER_NAME")

  DOMAIN_ROOT =  os.getenv("DOMAIN_ROOT")
  # DOMAIN_PORT =  os.getenv("DOMAIN_PORT")  
  DOMAIN_PORT =  formatEnvVar("DOMAIN_PORT", format_type='integer')

  # DOMAIN_NAME = os.getenv("DOMAIN_NAME")
  http_mode = "http"
  if config_docker != 'docker_on' : 
    if formatEnvVar("HTTPS_MODE", format_type='boolean') == True : 
      http_mode = "https"

    os.environ["SERVER_NAME"] = DOMAIN_ROOT + ":" + str(DOMAIN_PORT)
    os.environ["DOMAIN_NAME"] = http_mode + "://" + DOMAIN_ROOT + ":" + str(DOMAIN_PORT)
    DOMAIN_NAME =  os.getenv("DOMAIN_NAME")

  HTTPS_MODE = http_mode

  TEMPLATES_FOLDER   = "/templates"
  ROOT_FOLDER        = os.getcwd()
  UPLOADS_FOLDER     = ROOT_FOLDER+"/uploads"
  UPLOADS_IMAGES     = UPLOADS_FOLDER+"/img"
  UPLOADS_DATA       = UPLOADS_FOLDER+"/data_sources"
  
  # used for encryption and session management

  """ AUTH MODE """
  AUTH_MODE = os.getenv("AUTH_MODE")

  if AUTH_MODE != 'internal' :

    AUTH_URL_ROOT_LOCAL = os.getenv("AUTH_URL_ROOT_LOCAL")
    AUTH_URL_ROOT_DISTANT_PROD = os.getenv("AUTH_URL_ROOT_DISTANT_PROD")
    AUTH_URL_ROOT_DISTANT_PREPOD = os.getenv("AUTH_URL_ROOT_DISTANT_PREPOD")

    AUTH_URL_HEADERS = formatEnvVar('AUTH_URL_HEADERS', format_type='dict')
    AUTH_URL_HEADERS_PAYLOAD = formatEnvVar('AUTH_URL_HEADERS_PAYLOAD', format_type='dict')
    AUTH_URL_TOKEN_LOCATION = formatEnvVar('AUTH_URL_TOKEN_LOCATION', format_type='list')
    AUTH_URL_TOKEN_HEADER_NAME = os.getenv('AUTH_URL_TOKEN_HEADER_NAME')
    AUTH_URL_TOKEN_HEADER_TYPE = formatEnvVar('AUTH_URL_TOKEN_HEADER_TYPE', format_type='string')

    AUTH_URL_TOKEN_QUERY_STRING_NAME = os.getenv('AUTH_URL_TOKEN_QUERY_STRING_NAME', 'token')

    AUTH_DISTANT_ENDPOINTS = {
      
      ### LISTING USERS
      "users_list" : {
        "get_one" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_GET_ONE"),
          "method" :      os.getenv("AUTH_DISTANT_USER_GET_ONE_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_GET_ONE_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_GET_ONE_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_GET_ONE_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_GET_ONE_RESP', format_type='dict'),
        },
        "get_list"    : {
          "url" :         os.getenv("AUTH_DISTANT_USER_GET_LIST"),
          "method" :      os.getenv("AUTH_DISTANT_USER_GET_LIST_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_GET_LIST_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_GET_LIST_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_GET_LIST_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_GET_LIST_RESP', format_type='dict'),
        },
      },

      ### EDIT USER
      "user_edit" : {
        "register" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_REGISTER"),
          "method" :      os.getenv("AUTH_DISTANT_USER_REGISTER_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_REGISTER_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_REGISTER_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_REGISTER_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_REGISTER_RESP', format_type='dict'),
        },
        "confirm_email" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_CONF_EMAIL"),
          "method" :      os.getenv("AUTH_DISTANT_USER_CONF_EMAIL_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_CONF_EMAIL_RESP', format_type='dict'),
        },
        "user_update" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_EDIT"),
          "method" :      os.getenv("AUTH_DISTANT_USER_EDIT_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_EDIT_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_EDIT_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_EDIT_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_EDIT_RESP', format_type='dict'),
        },
        "user_delete" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_DELETE"),
          "method" :      os.getenv("AUTH_DISTANT_USER_DELETE_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_DELETE_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_DELETE_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_DELETE_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_DELETE_RESP', format_type='dict'),
        },
      },
      ###
      "user_login" : {
        "login" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_LOGIN"),
          "method" :      os.getenv("AUTH_DISTANT_USER_LOGIN_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_LOGIN_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_LOGIN_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_RESP', format_type='dict'),
        },
        "login_anonymous" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_LOGIN_ANO"),
          "method" :      os.getenv("AUTH_DISTANT_USER_LOGIN_ANO_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_LOGIN_ANO_RESP', format_type='dict'),
        },
      },
      ###
      "auth_tokens" : {
        "confirm_access" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_TOK_CONFIRM"),
          "method" :      os.getenv("AUTH_DISTANT_USER_TOK_CONFIRM_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CONFIRM_RESP', format_type='dict'),
        },
        "fresh_access_token" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_TOK_FRESH"),
          "method" :      os.getenv("AUTH_DISTANT_USER_TOK_FRESH_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_FRESH_RESP', format_type='dict'),
        },
        "new_access_token" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_TOK_NEW"),
          "method" :      os.getenv("AUTH_DISTANT_USER_TOK_NEW_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_RESP', format_type='dict'),
        },
        "new_refresh_token" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_TOK_NEW_REFRESH"),
          "method" :      os.getenv("AUTH_DISTANT_USER_TOK_NEW_REFRESH_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_NEW_REFRESH_RESP', format_type='dict'),
        },
        "token_claims" : {
          "url" :         os.getenv("AUTH_DISTANT_USER_TOK_CLAIMS"),
          "method" :      os.getenv("AUTH_DISTANT_USER_TOK_CLAIMS_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_POST_ARGS', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_URL_APPEND', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_USER_TOK_CLAIMS_RESP', format_type='dict'),
        },
      },
      ###
      "auth_password" : {
        "pwd_forgot" : {
          "url" :         os.getenv("AUTH_DISTANT_PWD_FORGOT"),
          "method" :      os.getenv("AUTH_DISTANT_PWD_FORGOT_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_FORGOT_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_FORGOT_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_FORGOT_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_FORGOT_RESP', format_type='dict'),
        },
        "pwd_reset" : {
          "url" :         os.getenv("AUTH_DISTANT_PWD_RESET"),
          "method" :      os.getenv("AUTH_DISTANT_PWD_RESET_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_RESET_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_RESET_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_RESP', format_type='dict'),
        },
        "pwd_reset_link" : {
          "url" :         os.getenv("AUTH_DISTANT_PWD_RESET_LINK"),
          "method" :      os.getenv("AUTH_DISTANT_PWD_RESET_LINK_METHOD"),
          "url_args" :    formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_URL_ARGS', format_type='dict'),
          "url_append" :  formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_URL_APPEND', format_type='list'),
          "post_args" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_POST_ARGS', format_type='dict'),
          "resp_path" :   formatEnvVar('AUTH_DISTANT_PWD_RESET_LINK_RESP', format_type='dict'),
        },
      }
    }

  """ OPTIONS ENCRYPTION / PROTECTION """
  RSA_MODE       = os.getenv('RSA_MODE')
  ANOJWT_MODE    = os.getenv('ANOJWT_MODE')
  ANTISPAM_MODE  = os.getenv('ANTISPAM_MODE')
  ANTISPAM_VALUE = os.getenv('ANTISPAM_VALUE')
  HTTPS_MODE     = os.getenv('HTTPS_MODE')

  """ RESTPLUS CONFIG """
  SWAGGER_UI_DOC_EXPANSION    = 'list'
  SWAGGER_UI_JSONEDITOR       = True
  SWAGGER_UI_OPERATION_ID     = True
  SWAGGER_UI_REQUEST_DURATION = True

  """ APP SECRET KEY """
  SECRET_KEY = os.getenv("SECRET_KEY") # "app_very_secret_key"

  """ SHARED JWT SECRET KEY : this key must be shared with openscraper and solidata """
  JWT_SECRET_KEY        = os.getenv("JWT_SECRET_KEY") # "a_key_youhouuuuuuu"

  JWT_HEADER_NAME       = os.getenv("JWT_HEADER_NAME") # "Authorization" #"X-API-KEY"
  JWT_TOKEN_LOCATION    = formatEnvVar("JWT_TOKEN_LOCATION", format_type="list") # ["headers", "query_string"]
  JWT_QUERY_STRING_NAME = os.getenv("JWT_HEADER_NAME") # "token"

  # beware not putting anything in JWT_HEADER_TYPE like 'Bearer', 
  # otherwise @jwt_required will look for an Authorization : Bearer <JWT> / 
  # not very comptatible with Flask-RestPlus authorization schemas described in _auth.authorizations.py
  JWT_HEADER_TYPE = "" 

  JWT_ACCESS_TOKEN_EXPIRES  = timedelta(minutes=720) # minutes=15

  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=10*365)  

  # JWT_IDENTITY_CLAIM  = "_id"
  ### custom JWT expirations
  JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES", format_type='integer')
  JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES      = timedelta(minutes=JWT_ANONYMOUS_REFRESH_TOKEN_EXPIRES_VAL)

  JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES", format_type='integer')
  JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES      = timedelta(days=JWT_CONFIRM_EMAIL_REFRESH_TOKEN_EXPIRES_VAL)

  JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES_VAL  = formatEnvVar("JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES", format_type='integer')
  JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES      = timedelta(days=JWT_RESET_PWD_ACCESS_TOKEN_EXPIRES_VAL)  



  # JWT_RENEW_REFRESH_TOKEN_AT_LOGIN = True 
  JWT_RENEW_REFRESH_TOKEN_AT_LOGIN = formatEnvVar('JWT_RENEW_REFRESH_TOKEN_AT_LOGIN', format_type='boolean') # False 


  """ MONGODB """
  # MONGO_URI  = 'mongodb://localhost:27017/solidata'
  MONGO_URI  = os.getenv("MONGODB_URI")

  # collections
  MONGO_COLL_TAGS                 = os.getenv("MONGO_COLL_TAGS", "tags")
  MONGO_COLL_USERS                = os.getenv("MONGO_COLL_USERS", "users")
  MONGO_COLL_PROJECTS             = os.getenv("MONGO_COLL_PROJECTS", "projects")
  MONGO_COLL_DATAMODELS_TEMPLATES = os.getenv("MONGO_COLL_DATAMODELS_TEMPLATES", "datamodels_templates")
  MONGO_COLL_DATAMODELS_FIELDS    = os.getenv("MONGO_COLL_DATAMODELS_FIELDS", "datamodels_fields")
  # MONGO_COLL_CONNECTORS         = os.getenv("MONGO_COLL_CONNECTORS", "connectors")
  MONGO_COLL_DATASETS_INPUTS      = os.getenv("MONGO_COLL_DATASETS_INPUTS", "datasets_inputs")
  MONGO_COLL_DATASETS_INPUTS_DOC  = os.getenv("MONGO_COLL_DATASETS_INPUTS_DOC", "datasets_inputs_docs")
  MONGO_COLL_DATASETS_RAWS        = os.getenv("MONGO_COLL_DATASETS_RAWS", "datasets_raws")
  MONGO_COLL_DATASETS_OUTPUTS     = os.getenv("MONGO_COLL_DATASETS_OUTPUTS", "datasets_outputs")
  MONGO_COLL_DATASETS_OUTPUTS_DOC = os.getenv("MONGO_COLL_DATASETS_OUTPUTS_DOC", "datasets_outputs_docs")
  MONGO_COLL_RECIPES              = os.getenv("MONGO_COLL_RECIPES", "recipes")
  # MONGO_COLL_CORR_DICTS         = os.getenv("MONGO_COLL_CORR_DICTS", "corr_dicts")
  MONGO_COLL_LICENCES             = os.getenv("MONGO_COLL_LICENCES", "licences")
  MONGO_COLL_JWT_BLACKLIST        = os.getenv("MONGO_COLL_JWT_BLACKLIST", "jwt_blacklist")


  """ EMAILING """
  # # email server
  MAIL_SERVER        = os.getenv('MAIL_SERVER') # 'smtp.googlemail.com'
  MAIL_PORT          = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True
  MAIL_USERNAME      = os.getenv('MAIL_USERNAME') # "XXX.XXX@XXX.com" # os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD      = os.getenv('MAIL_PASSWORD') # "XXXXX" # os.environ.get('MAIL_PASSWORD')

  # administrator list
  ADMINS              = formatEnvVar('MAIL_ADMINS', format_type='list') # ['XXXX.XXXX@gmail.com']
  MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') # 'XXXX.XXXX@gmail.com'

  """ ENCRYPTION FOR CONFIRMATION EMAIL """
  # SECURITY_PASSWORD_SALT   = 'my_precious_salt_security'
  SECURITY_PASSWORD_SALT   = os.getenv('SECURITY_PASSWORD_SALT') # 'XXXXXXX'




class Preprod(BaseConfig) : 


  REDIRECTION_FRONT  = os.getenv('REDIRECTION_FRONT_PREPROD')# "http://preprod.toktok.co-demos.com" 

  # """ EMAILING """
  # MAIL_PORT        = 587
  # MAIL_PORT        = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  # MAIL_USE_TLS     = True
  # MAIL_USE_SSL     = False
  # MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  # MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True

  """ HOST - prod IP and domain name"""
  SERVER_NAME_TEST   = "True" 



class Prod(BaseConfig) : 


  REDIRECTION_FRONT    = os.getenv('REDIRECTION_FRONT_PROD')# "http://toktok.co-demos.com" 

  # """ EMAILING """
  # MAIL_PORT        = 587
  # MAIL_PORT          = formatEnvVar('MAIL_PORT', format_type='integer') # 465
  # MAIL_USE_TLS     = True
  # MAIL_USE_SSL     = False
  # MAIL_USE_TLS       = formatEnvVar('MAIL_USE_TLS', format_type='boolean') # False
  # MAIL_USE_SSL       = formatEnvVar('MAIL_USE_SSL', format_type='boolean') # True

  """ HOST - prod IP and domain name"""
  SERVER_NAME_TEST   = "True" 