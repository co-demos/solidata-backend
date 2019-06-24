# -*- encoding: utf-8 -*-

"""
endpoint_usr_edit.py  
"""

from solidata_api.api import *

log.debug(">>> api_usr ... creating api endpoints for USR_EDIT")

from . import api, document_type

### create namespace
ns = Namespace('edit', description="Users : user's info edition related endpoints")

### import models 
from solidata_api._models.models_updates import * 
from solidata_api._models.models_user import *  
model_doc 				= User_infos(ns)
model_doc_out			= model_doc.model_complete_out
model_doc_guest_out		= model_doc.model_guest_out
model_doc_min			= model_doc.model_minimum
models 				= {
  "model_doc_out" 		: model_doc_out ,
  "model_doc_guest_out" 	: model_doc_guest_out ,
  "model_doc_min" 		: model_doc_min ,
} 
model_data				= UserData(ns).model

model_update	= Update_infos(ns, document_type).model_update_generic

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES 
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route("/<string:usr_id>")
@ns.response(404, 'document not found')
@ns.param('usr_id', 'The user unique identifier')
class Usr_edit(Resource) :
  """
  usr edition :
  PUT    - Updates usr infos
  DELETE - Let you delete document
  """
  
  @ns.doc('update_usr')
  @current_user_required
  # @guest_required
  @ns.expect([model_update])
  @api.doc(params={'usr_id': 'the usr oid'})
  @distant_auth(func_name="update_user", return_resp=True, ns_payload=True )
  def put(self, usr_id):
    """
    Update a  usr in db

    >
      --- needs   : a valid access_token in the header, field_to_update, field_value
      >>> returns : msg, doc data 
    """
    
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### check client identity and claims
    claims = get_jwt_claims() 
    log.debug("claims : \n %s", pformat(claims) )

    ### update doc in DB
    updated_doc, response_code	= Query_db_update (
      ns, 
      models,
      document_type,
      usr_id,
      claims,
      roles_for_complete = ["admin"],
      payload = ns.payload
    )

    log.debug("updated_doc : \n%s ", pformat(updated_doc) )

    ### return updated document
    return updated_doc, response_code


  @ns.doc('delete_user')
  @ns.response(204, 'document deleted')
  @current_user_required
  @api.doc(params={'usr_id': 'the usr oid'})
  @distant_auth(func_name="delete_user", return_resp=True )
  def delete(self, usr_id):
    """
    Delete an user given its _id / only doable by admin or current_user
    
    > 
      --- needs   : a valid access_token (as admin or current user) in the header, an user_oid of the user in the request
      >>> returns : msg, response 204 as user is deleted

    """

    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    # log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### check client identity and claims
    claims = get_jwt_claims() 
    log.debug("claims : \n %s", pformat(claims) )

    ### query db from generic function 		
    results, response_code	= Query_db_delete (
      ns, 
      models,
      document_type,
      usr_id,
      claims,
      roles_for_delete 	= ["admin"],
      auth_can_delete 	= ["owner"],
    )

    log.debug("results : \n%s ", pformat(results) )

    return results, response_code
