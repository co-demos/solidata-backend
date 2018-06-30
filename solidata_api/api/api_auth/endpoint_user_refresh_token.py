# -*- encoding: utf-8 -*-

"""
endpoint_refresh_token.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log, pformat
log.debug(">>> api_users ... creating api endpoints for USER_REFRESH_TOKEN")


# from  datetime import datetime, timedelta
# from	bson import json_util
# from	bson.objectid import ObjectId
# from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource #, fields, marshal, reqparse
# from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import JWT utils
# import jwt
from flask_jwt_extended import (
		jwt_refresh_token_required, create_access_token,
		get_jwt_identity
)

### import mongo utils
# from solidata_api.application import mongo
from solidata_api._core.queries_db import mongo_users

### import auth utils
# from solidata_api._auth import token_required

# ### import data serializers
# from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('refresh', description='User refresh token ')

### import parsers
# from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
# from .models import * # model_user, model_new_user
from solidata_api._models.models_user import *  
model_user_access				= User_infos(ns).model_access


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html


@ns.route('/')
class Refresh(Resource) :

	# The jwt_refresh_token_required decorator insures a valid refresh
	# token is present in the request before calling this endpoint. We
	# can use the get_jwt_identity() function to get the identity of
	# the refresh token, and use the create_access_token() function again
	# to make a new access token for this identity.
	@ns.doc(security='apikey')
	@jwt_refresh_token_required
	def post(self) : 
		"""
		refresh the access token
		needs to send the refresh token
		in the header 
		"""

		### DEBUGGING
		print()
		print("-+- "*40)
		log.debug( "ROUTE class : %s", self.__class__.__name__ )
		log.debug ("payload : \n{}".format(pformat(ns.payload)))

		### retrieve current_user identity from refresh token
		current_user = get_jwt_identity()
		log.debug("current_user : \n %s", current_user)

		### retrieve user from db to get all infos
		user = mongo_users.find_one( {"infos.email" : current_user } )
		log.debug("user : \n %s", pformat(user)) 

		user_light 	= marshal( user , model_user_access)
		user_light["_id"] = str(user["_id"])

		### create new access token
		new_access_token = create_access_token(identity=user_light, fresh=False)
		
		### save new access token in user db
		# user["auth"]["acc_tok"] = new_access_token
		# mongo_users.save(user)

		token = {
				'access_token': new_access_token
		}
		
		return {	
							"msg" 		: "user -{}- has a new access token ".format(current_user) , 
							"tokens"	:  token
					}, 200