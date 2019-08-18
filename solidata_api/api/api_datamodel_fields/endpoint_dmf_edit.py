# -*- encoding: utf-8 -*-

"""
endpoint_dmf_edit.py  
"""

from solidata_api.api import *

log.debug(">>> api_dmf ... creating api endpoints for DMF_EDIT")

from . import api, document_type

### create namespace
ns = Namespace('edit', description='Edit a dmf : ... ')

### import models 
from solidata_api._models.models_updates import * 
from solidata_api._models.models_datamodel_field import * 
mod_doc             = Dmf_infos(ns)
model_doc_out       = mod_doc.mod_complete_out
model_doc_guest_out = mod_doc.model_guest_out
model_doc_min       = mod_doc.model_minimum
models              = {
  "model_doc_out"       : model_doc_out ,
  "model_doc_guest_out" : model_doc_guest_out ,
  "model_doc_min"       : model_doc_min ,
} 

model_update	= Update_infos(ns, document_type).model_update_generic

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

# cf : http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html


@ns.doc(security='apikey')
@ns.route('/<string:doc_id>')
@ns.response(404, 'document not found')
@ns.param('doc_id', 'The document unique identifier')
class Dmf_update(Resource):
  """
  dmf edition :
  PUT    - Updates document's infos
  DELETE - Let you delete document
  """


  @ns.doc('update_dmf')
  @guest_required 
  @ns.expect([model_update])
  @ns.doc(params={'doc_id': 'the dmf oid'})
  def put(self, doc_id):
    """
    Update a  dmf in db

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
    # claims = get_jwt_claims() 
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    ### update doc in DB
    updated_doc, response_code	= Query_db_update (
      ns, 
      models,
      document_type,
      doc_id,
      claims,
      roles_for_complete = ["admin"],
      payload = ns.payload
    )

    log.debug("updated_doc : \n%s ", pformat(updated_doc) )

    ### return updated document
    # return {
    # 	"msg" : "updating doc...."
    # }, 200
    return updated_doc, response_code









  @ns.doc('delete_dmf')
  @ns.response(204, 'document deleted')
  @guest_required 
  @ns.doc(params={'doc_id': 'the dmf oid'})
  def delete(self, doc_id):
    """
    delete a dmf in db

    > 
      --- needs   : a valid access_token (as admin or current user) in the header, an oid of the document in the request
      >>> returns : msg, response 204 as document is deleted

    """

    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    # log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### check client identity and claims
    # claims = get_jwt_claims() 
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    ### query db from generic function 		
    results, response_code	= Query_db_delete (
      ns, 
      models,
      document_type,
      doc_id,
      claims,
      roles_for_delete 	= ["admin"],
      auth_can_delete 	= ["owner"],
    )

    log.debug("results : \n%s ", pformat(results) )


    return results, response_code