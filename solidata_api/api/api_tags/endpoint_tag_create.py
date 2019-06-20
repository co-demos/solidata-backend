# -*- encoding: utf-8 -*-

"""
endpoint_tag_create.py  
"""

from solidata_api.api import *

log.debug(">>> api_tags ... creating api endpoints for TAG_CREATE")

from . import api, document_type

### create namespace
ns = Namespace('create', description='Tag : create a new tag ')

### import models 
from solidata_api._models.models_tag import *  
model_new_tag  	= NewTag(ns).model
model_tag		= Tag_infos(ns)
model_tag_in	= model_tag.model_complete_in
model_tag_out	= model_tag.model_complete_out

models 			= {
  "model_doc_in" 			: model_tag_in ,
  "model_doc_out" 		: model_tag_out 
} 



### CREATE DEFAULT TAGS FROM config_default_docs
### import default documents 
from solidata_api.config_default_docs import default_tag_list

for dft_tag in default_tag_list : 
  
  log.debug ("dft_tag : \n{}".format(pformat(dft_tag)))
  
  Query_db_insert(
    ns, 
    models,
    document_type,

    dft_tag,

    value_to_check 	= dft_tag["infos"]["title"],
    field_to_check	= "infos.title",

    user_role   	= "system"
  )





### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 






@ns.doc(security='apikey')
@ns.route('/')
class TagCreate(Resource):

  @ns.doc('tag_create')
  @guest_required 
  @ns.expect(model_new_tag, validate=True)
  # @ns.marshal_with(model_tag_in) #, envelope="new_tag", code=201)
  def post(self):
    """
    Create a new tag in db

    >
      --- needs   : a valid access_token in the header
      >>> returns : msg, tag data 
    """
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### check client identity and claims
    claims 			= get_jwt_claims() 
    log.debug("claims : \n %s", pformat(claims) )
    
    # user_id 		= get_jwt_identity() ### get the oid as str
    # log.debug('user_identity from jwt : \n%s', user_identity )  
    user_id 		= claims["_id"]
    user_oid		= ObjectId(user_id)
    # user_role 		= claims["auth"]["role"]

    ### get data from form and preload for marshalling
    new_tag_infos = { 
      "infos" 		: ns.payload,
      "public_auth" 	: ns.payload,
      "specs"			: {
        "doc_type" : "tag"
      },
    }

    ### marshall infos with dmt complete model
    new_tag 		= marshal( new_tag_infos , model_tag_in)
    log.debug('new_dmt : \n%s', pformat(new_tag) )  
    
    ### complete missing default fields
    new_tag_auto_fields = { 
      "log"			: { 
        "created_at"	: datetime.utcnow(),
        "created_by"	: user_oid,
      },
      "uses"			: {
        "by_usr"		: [ 
          {
            "used_by" : user_oid,
            "used_at" : [ 
              # { "at" : datetime.utcnow() } 
              datetime.utcnow() 
            ]
          } 
        ]
      },
      "team"			: [ 
        {
          'oid_usr'	: user_oid,
          'edit_auth'	: "owner",
          'added_at'  : datetime.utcnow(),
          'added_by'  : user_oid,
        }
      ],
    }
    log.debug('new_tag_infos : \n%s', pformat(new_tag_infos) )  

    ### update marshalled infos by concatenating with auto fields
    new_tag 	= { **new_tag, **new_tag_auto_fields }
    log.debug('new_tag : \n%s', pformat(new_tag) )  

    ### save new_dmt in db 
    _id = mongo_tags.insert( new_tag )
    log.info("new_tag has being created and stored in DB ...")
    log.info("_id : \n%s", pformat(_id) )

    ### add _id as string to data
    new_tag["_id"] = str(_id)
    log.debug('new_tag : \n%s', pformat(new_tag) )  

    ### marshall out the saved item as complete data
    new_tag_out = marshal( new_tag , model_tag_out)
    log.debug('new_tag_out : \n%s', pformat(new_tag_out) )  

    return { 
      "msg"	: "dear user, there is the tag you just created... ", 
      "data" 	: new_tag_out
    }, 200







