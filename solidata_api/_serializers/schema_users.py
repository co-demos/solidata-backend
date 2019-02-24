# -*- encoding: utf-8 -*-

"""
schema_users.py  
- provides the model for USER definition in DB and Flask-Restplus
"""

from log_config import log, pformat

log.debug("... loading schema_users.py ...")

from flask_restplus import fields 

from solidata_api._choices import * 
from .schema_generic import *
from .schema_logs import *


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### basic informations about a user
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
name 				= fields.String(
										description	= "name of the user",
										attribute		= "name",
										example			= "Elinor",
										default			= 'Anonymous User',
										required		= False,
									)
pseudo 				= fields.String(
										description	= "pseudo of the user",
										attribute		= "pseudo",
										example			= "Coco",
										default			= 'Anonymous User',
										required		= False,
									)
surname 			= fields.String(
										description 	= "surname of the user",
										attribute		= "surname",
										example			= "Ostrom",
										required 		= False,
									)
email 				= fields.String(
										description 	= "email of the user",
										attribute		= "email",
										example			= "elinor.ostrom@emailna.co", ### uses https://www.mohmal.com for temporary emails
										required		= True,
									)
agreement			= fields.Boolean(
										description	= "user has agreed to terms and conditions",
										attribute		= "agreement",
										example			= False,
										required		= False,
										default			= False,
									)
email_encrypt 		= fields.String(
										description 	= "email of the user",
										attribute		= "email_encrypt",
										example			= "elinor.ostrom@emailna.co", ### uses https://www.mohmal.com for temporary emails
										required		= True,
									)
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### auth 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
pwd					= fields.String(
										description 	= "password of the user",
										attribute		= "pwd",
										example			= "a-very-common-password",
										required		= True,
									)
pwd_encrypt			= fields.String(
										description 	= "password of the user hashed from frontend with access_token",
										attribute		= "pwd_encrypt",
										example			= "hashed-common-password",
										required		= False,
									)
confirmed_usr		= fields.Boolean(
										description	= "user has confirmed its account from his email",
										attribute		= "conf_usr",
										example			= False,
										required		= False,
										default			= False,
									)
is_blacklisted		= fields.Boolean(
										description	= "user has confirmed its account from his email",
										attribute		= "is_blacklisted",
										example			= False,
										required		= False,
										default			= False,
									)
role				= fields.String(
										description 	= "role / authorization level of the user",
										attribute		= "role",
										example			= "guest",
										enum			= user_roles,
										default			= "guest",
										required		= True,
									)
acc_tok				= fields.String(
										description 	= "access token of user",
										attribute		= "acc_tok",
										example			= "a-json-web-access-token",
										default			= "no_access_token",
									)
refr_tok			= fields.String(
										description	= "refresh token of user",
										attribute		= "refr_tok",
										example			= "a-json-web-refresh-token",
										default			= "no_refresh_token",
									)
old_refr_tok		= fields.String(
										description	= "expired refresh token of user",
										attribute		= "old_refr_tok",
										example			= "an-old-json-web-refresh-token",
										default			= "no_old_refresh_token",
										required		= False,
									)
# edit_auth			= fields.List(
# 										fields.String(
# 											description = "edit auth of an user",
# 											enum		= user_actions_proj,
# 										),
# 										required		= False,
# 										attribute		= "edit_auth", 
# 										default			= [] 
# 									)
# edit_auth			= fields.String(
# 										description 	= "edit auth of an user",
# 										enum			= user_edit_auth,
# 										example			= "can_only_view",
# 										required		= False,
# 										attribute		= "edit_auth", 
# 										default			= [] 
# 									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### profile
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
language			= fields.String(
										description 	= "language preference", 
										example 		= "en",
										attribute		= "lang",	
										default			= "en",
										required		= True,
									)
is_fav				= fields.Boolean(
										description	= "is the document a favorite ?",
										attribute		= "is_fav",
										example			= False,
										required		= True,
										default			= False,
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### professional infos
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
struct_name			= fields.String(
										description	= "name of the user's structure",
										attribute		= "struct_name",
										required		= True,
									)
struct_profile		= fields.String(
										description	= "profile of the structure",
										attribute		= "struct_profile",
										example			= "public_state",
										enum			= user_structure,
										required		= False,
									)
struct_url 			= fields.String(
										description	= "structure url link",
										attribute		= "struct_url",
										example			= "my-url-link",
										default			= '',
										required		= False,
									)

usr_profile			= fields.String(
										description	= "profiles of the user",
										enum			= user_profiles,
									)
usr_profiles		= fields.List(
										usr_profile,
										example			= ["organizer"],
										attribute		= "profiles",	
										default			= []
									)

usr_view			= fields.String(
										description	= "view of the user : which collections are visible in front",
										enum			= user_view,
										attribute		= "usr_view",
										default			= 'minimal',
									)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FOR GENERIC MODELS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
user_data = {
	"data" 				: generic_data,
}

user_identity = {
	"email" 			: email,
}

user_pwd = {
	"pwd"		 		: pwd,
}
user_pwd_encrypted = {
	"pwd_encrypt"		: pwd_encrypt,
}

# user_login = {
# 	# "email" 			: email,
# 	# "pwd"				: pwd,
# 	"email_encrypt" 	: email_encrypt,
# 	"pwd_encrypt"		: pwd_encrypt,
# }
user_login = {
	"email_encrypt" : email_encrypt,
	"pwd_encrypt"		: pwd_encrypt,
}
user_login_nosalt = {
	"email" 		: email,
	"pwd"				: pwd,
}

user_basics = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
	"pseudo"			: pseudo,
}
user_basics_light = {
	"pseudo"			: name,
}

# user_register = {
# 	"name" 				: name,
# 	"surname" 			: surname,
# 	# "email" 			: email,
# 	"email_encrypt" 	: email_encrypt,
# 	# "pwd"				: pwd,
# 	"pwd_encrypt"		: pwd_encrypt,
# 	"lang"				: language,
# 	"agreement"			: agreement,
# }
user_register = {
	"name" 					: name,
	"surname" 			: surname,
	"email_encrypt" : email_encrypt,
	"pwd_encrypt"		: pwd_encrypt,
	"lang"					: language,
	"agreement"			: agreement,
}
user_register_nosalt = {
	"name" 				: name,
	"surname" 		: surname,
	"email" 			: email,
	"pwd"					: pwd,
	"lang"				: language,
	"agreement"		: agreement,
}

old_refresh_token = {
	"old_refresh_token"	: old_refr_tok,
}


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FOR MODELS TO INSERT IN DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
user_auth_in = {
	"pwd"							: pwd,
	"conf_usr"				: confirmed_usr,
	"role"						: role,
	# "acc_tok"				: acc_tok,
	"refr_tok"				: refr_tok,
	"is_blacklisted"	: is_blacklisted,
}

usr_profile_ = {
	"lang"  				: language,
	"agreement"			: agreement,
	"usr_view"			: usr_view,
	"usr_profiles"	: usr_profiles,
}

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FOR MODELS TO EXPORT OUT OF DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
user_auth_out = {
	# "pwd"					: pwd,
	"role"					: role,
	"conf_usr"			: confirmed_usr,
	# "acc_tok"			: acc_tok,
}

user_struct = {
	"struct_name" 		: struct_name,
	"struct_profile"	: struct_profile,
	"struct_url"			: struct_url,
}
