# -*- encoding: utf-8 -*-

"""
endpoint_users.py  
- provides the API endpoints for consuming and producing
	REST requests and responses
"""

from log_config import log
log.debug(">>> api_users ... creating api endpoints for USERS")

from	bson import json_util
from	bson.objectid import ObjectId
from	bson.json_util import dumps

from flask import current_app, request
from flask_restplus import Namespace, Resource, fields, marshal, reqparse
from 	werkzeug.security 	import 	generate_password_hash, check_password_hash

### import mongo utils
from solidata_api.application import mongo
from solidata_api._core.queries_db import * # mongo_users, etc...

### import auth utils
from solidata_api._auth import token_required

# ### import data serializers
from solidata_api._serializers.schema_users import *  

### create namespace
ns = Namespace('users', description='Users list ')

### import parsers
from solidata_api._parsers.parser_pagination import pagination_arguments

### import models 
from .models import * # model_user, model_new_user
model_new_user  = NewUser(ns).model
model_user      = User(ns).model


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

@ns.route('/')
class UsersList(Resource):

	@ns.doc('users_list')
	@token_required
	@ns.expect(pagination_arguments)
	@ns.marshal_list_with( model_user, skip_none=True)#, envelop="users_list" ) 
	def get(self):
		"""
		list of all users in db 
		without _id 
		"""
		### DEBUGGING
		print()
		log.debug( self.__class__.__name__ )

		### get pagination
		args = pagination_arguments.parse_args(request)
		page = args.get('page', 1)
		per_page = args.get('per_page', 10)

		### retrieve from db
		cursor = mongo_users.find({}, {"_id": 0 })
		users = list(cursor)
		log.debug( users )

		return users, 200


	@ns.doc('create_user')
	@ns.expect(model_new_user, validate=True)
	@ns.marshal_with(model_new_user, envelope="new_user", code=201)
	def post(self):
			"""
			create / register a new user
			"""
			print()
			log.debug("post")
			log.debug ("payload : \n{}".format(pformat(ns.payload)))

			payload_email = ns.payload["email"]
			log.debug("email : %s", payload_email )

			### chek if user already exists in db
			existing_user = mongo_users.find_one({"infos.email" : payload_email})
			log.debug(existing_user)

			if existing_user is None :

				payload_pwd = ns.payload["password"]
	
				new_user = marshal(ns.payload, model_user)
				log.debug ("new_user : \n{}".format(pformat(new_user)))

				# create hashpassword
				hashpass = generate_password_hash(payload_pwd, method='sha256')
				
				return "new user added... (fake)"
			
			else :
				
				return "this email already exists"




