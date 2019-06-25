# -*- encoding: utf-8 -*-

"""
_core/queries_db/__init__.py  
"""

import pandas as pd

from log_config import log, pformat
print()
log.debug(">>> _core.queries_db.__init__.py ..." )
log.debug(">>> queries_db ... loading mongodb collections as global variables")

from flask import current_app as app

from solidata_api.application import mongo



### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL VARIABLES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

### declaring collections as app variables

mongo_tags 									= mongo.db[ app.config["MONGO_COLL_TAGS"] ]
mongo_users 								= mongo.db[ app.config["MONGO_COLL_USERS"] ]
mongo_projects 							= mongo.db[ app.config["MONGO_COLL_PROJECTS"] ]
mongo_datamodels_templates 	= mongo.db[ app.config["MONGO_COLL_DATAMODELS_TEMPLATES"] ]
mongo_datamodels_fields 		= mongo.db[ app.config["MONGO_COLL_DATAMODELS_FIELDS"] ]
# mongo_connectors	 				= mongo.db[ app.config["MONGO_COLL_CONNECTORS"] ]
mongo_datasets_inputs 			= mongo.db[ app.config["MONGO_COLL_DATASETS_INPUTS"] ]
mongo_datasets_inputs_docs 	= mongo.db[ app.config["MONGO_COLL_DATASETS_INPUTS_DOC"] ]
mongo_datasets_raws 				= mongo.db[ app.config["MONGO_COLL_DATASETS_RAWS"] ]
mongo_recipes 							= mongo.db[ app.config["MONGO_COLL_RECIPES"] ]
# mongo_corr_dicts 					= mongo.db[ app.config["MONGO_COLL_CORR_DICTS"] ]
mongo_datasets_outputs 			= mongo.db[ app.config["MONGO_COLL_DATASETS_OUTPUTS"] ]
mongo_datasets_outputs_doc 	= mongo.db[ app.config["MONGO_COLL_DATASETS_OUTPUTS_DOC"] ]

mongo_licences 							= mongo.db[ app.config["MONGO_COLL_LICENCES"] ]
mongo_jwt_blacklist 				= mongo.db[ app.config["MONGO_COLL_JWT_BLACKLIST"] ]


### TEMPORARY WHILE ADDING DSI_DOCS PROCESSES
log.debug(">>> _core.queries_db.__init__.py / COPYING EACH DSI.data_raw.f_data to DSI_DOCS as documents... " )
all_dsi = list(mongo_datasets_inputs.find({}))

for dsi in all_dsi : 

	oid_dsi = dsi["_id"]
	dsi_docs = mongo_datasets_inputs_docs.find( {"_id" : oid_dsi} )
	
	if dsi_docs == None:
		### get f_data
		dsi_f_data = dsi["data_raw"]["f_data"]

		### convert existing list to dataframe
		df_ = pd.DataFrame(dsi_f_data)
		df_["oid_dsi"] = oid_dsi
		df_col_dict_ = df_.to_dict(orient="records")

		### insert many docs in dso_docs for every entry of df_col_dict
		log.info("inserting documents related to dsi in mongo_datasets_inputs_docs ...")
		if len(df_col_dict_) > 0 and len(df_col_dict_) < 2 :
			mongo_datasets_inputs_docs.insert_one( df_col_dict_ )
		else :
			mongo_datasets_inputs_docs.insert_many( df_col_dict_ )

		### TO DO 
		### delete f_data entry from dsi
		# dsi["data_raw"]["f_data"] = None

log.debug(">>> _core.queries_db.__init__.py / INDEXING COLLECTIONS ... " )

### drop previous text indexes (only one text index per collection)
main_text_fields_to_drop = '$**_text'
try :
	mongo_tags.drop_index(main_text_fields_to_drop)
	mongo_users.drop_index(main_text_fields_to_drop)
	mongo_projects.drop_index(main_text_fields_to_drop)
	mongo_datamodels_templates.drop_index(main_text_fields_to_drop)
	mongo_datamodels_fields.drop_index(main_text_fields_to_drop)
	mongo_datasets_inputs.drop_index(main_text_fields_to_drop)
	mongo_datasets_inputs_docs.drop_index(main_text_fields_to_drop)
	mongo_datasets_raws.drop_index(main_text_fields_to_drop)
	mongo_recipes.drop_index(main_text_fields_to_drop)
	mongo_datasets_outputs.drop_index(main_text_fields_to_drop)
	mongo_datasets_outputs_doc.drop_index(main_text_fields_to_drop)
	mongo_licences.drop_index(main_text_fields_to_drop)
	mongo_jwt_blacklist.drop_index(main_text_fields_to_drop)
except:
	pass

# # create index for every collection needing it  
# # cf : https://api.mongodb.com/python/current/api/pymongo/collection.html?highlight=drop#pymongo.collection.Collection.create_index
# # cf : https://code.tutsplus.com/tutorials/full-text-search-in-mongodb--cms-24835 
# # cf (in open scraper) : self.coll_data.create_index([('$**', 'text')])
all_text_fields_index_name	= "all_fields"
all_text_fields_to_index 	= [('$**', 'text')]

main_text_fields_index_name	 = "main_fields"
main_text_fields_to_index = [
	("infos.title"				,"text") ,
	("infos.description"	,"text") ,
	("infos.licence"			,"text") ,
	("data_raw.f_code"		,"text") ,
	("data_raw.f_object"	,"text") ,
	("data_raw.f_code"		,"text") ,
	("data_raw.f_comments","text") ,
	("data_raw.f_data"		,"text") ,
	("data_raw.f_code"		,"text") ,
]

log.debug(">>> _core.queries_db.__init__.py / INDEXING COLLECTIONS : all fields... " )
mongo_datasets_inputs.create_index(				all_text_fields_to_index, name=all_text_fields_index_name) 	### index all fields
mongo_datasets_inputs_docs.create_index(	all_text_fields_to_index, name=all_text_fields_index_name) 	### index all fields
mongo_datasets_raws.create_index(					all_text_fields_to_index, name=all_text_fields_index_name)	### index all fields
mongo_datasets_outputs.create_index(			all_text_fields_to_index, name=all_text_fields_index_name) 	### index all fields
mongo_datasets_outputs_doc.create_index(	all_text_fields_to_index, name=all_text_fields_index_name) 	### index all fields

log.debug(">>> _core.queries_db.__init__.py / INDEXING COLLECTIONS : main fields... " )
mongo_users.create_index(									main_text_fields_to_index, name=main_text_fields_index_name)
mongo_tags.create_index(									main_text_fields_to_index, name=main_text_fields_index_name)
mongo_projects.create_index(							main_text_fields_to_index, name=main_text_fields_index_name)
mongo_datamodels_templates.create_index(	main_text_fields_to_index, name=main_text_fields_index_name)
mongo_datamodels_fields.create_index(			main_text_fields_to_index, name=main_text_fields_index_name)
mongo_recipes.create_index(								main_text_fields_to_index, name=main_text_fields_index_name)

mongo_licences.create_index(							main_text_fields_to_index, name=main_text_fields_index_name)
mongo_jwt_blacklist.create_index(					main_text_fields_to_index, name=main_text_fields_index_name)


db_dict = {
	"mongo_tags"									: mongo_tags,
	"mongo_users"									: mongo_users,
	"mongo_projects"							: mongo_projects,
	"mongo_datamodels_templates"	: mongo_datamodels_templates,
	"mongo_datamodels_fields"			: mongo_datamodels_fields,
	# "mongo_connectors"					: mongo_connectors,

	"mongo_datasets_inputs"				: mongo_datasets_inputs,
	"mongo_datasets_inputs_docs"	: mongo_datasets_inputs_docs,

	"mongo_datasets_raws"					: mongo_datasets_raws,
	"mongo_recipes"								: mongo_recipes,
	# "mongo_corr_dicts"					: mongo_corr_dicts,

	"mongo_datasets_outputs"			: mongo_datasets_outputs,
	"mongo_datasets_outputs_doc"	: mongo_datasets_outputs_doc,

	"mongo_licences"							: mongo_licences,
	"mongo_jwt_blacklist"					: mongo_jwt_blacklist,
}
db_dict_by_type = {
	"tag" : mongo_tags,
	"usr" : mongo_users,
	"prj" : mongo_projects,
	"dmt" : mongo_datamodels_templates,
	"dmf" : mongo_datamodels_fields,
	"dsi" : mongo_datasets_inputs,
	"dsi_doc" : mongo_datasets_inputs_docs,
	"dsr" : mongo_datasets_raws,
	"rec" : mongo_recipes,

	"dso" : mongo_datasets_outputs,
	"dso_doc"	: mongo_datasets_outputs_doc,

	"lic" : mongo_licences,
	"jwt_blacklist" : mongo_jwt_blacklist,
}

def select_collection(coll_name):
	coll = db_dict[coll_name]
	return coll


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### SERIALIZERS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
class Marshaller :

	def __init__( self, ns, models ):
		
		self.ns 									= ns
		self.model_doc_out 				= models["model_doc_out"]
		self.model_doc_guest_out 	= models["model_doc_guest_out"]
		self.model_doc_min		 		= models["model_doc_min"]

		self.results_list					= None 

	def marshal_as_complete (self, results_list ) :

		ns = self.ns
		self.results_list = results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_guest (self, results_list ) :
	
		ns = self.ns
		self.results_list = results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_guest_out)
		def get_results():
			return results_list
		return get_results()

	def marshal_as_min (self, results_list ) :
	
		ns = self.ns
		self.results_list = results_list
		log.debug('results_list ...' )  
		# log.debug('results_list : \n%s', pformat(results_list[:1]) )  
		
		@ns.marshal_with(self.model_doc_min)
		def get_results():
			return results_list
		return get_results()


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FINAL IMPORTS FOR QUERIES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

from .query_utils import *
from .query_doc import *
from .query_stats import *
from .query_list import *
from .query_delete import *
from .query_update import *
from .query_solidify import *
from .query_insert_doc import *
from .query_build_dso import *

print()




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