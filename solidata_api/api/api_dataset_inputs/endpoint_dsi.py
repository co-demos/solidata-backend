# -*- encoding: utf-8 -*-

"""
endpoint_dsi.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI")

from . import api, document_type

### create namespace
ns = Namespace('infos', description='Dataset inputs : request and list all dsi infos')

### import models 
from solidata_api._models.models_dataset_input import * 
mod_doc							= Dsi_infos(ns)
model_doc_out				= mod_doc.mod_complete_out
model_doc_guest_out	= mod_doc.model_guest_out
model_doc_min				= mod_doc.model_minimum
models 							= {
  "model_doc_out" 			: model_doc_out ,
  "model_doc_guest_out" : model_doc_guest_out ,
  "model_doc_min" 			: model_doc_min ,
} 

from solidata_api._models.models_stats import *
mod_stats       = Stats_query(ns, document_type)
mod_stats_query = mod_stats.model_stats_query


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 







@ns.route("/get_one/<string:doc_id>")
class Dsi_infos_(Resource):
  
  @ns.doc('dsi_infos')
  # @ns.expect(query_arguments)
  @ns.expect(query_pag_args, query_data_dsi_arguments)
  # @jwt_optional
  @jwt_optional_sd
  @ns.doc(params={'doc_id': 'the dataset input oid'})
  def get(self, doc_id):
    """
    get infos of a specific dsi in db

    :param doc_id : dsi's oid <doc_id>

    >
      --- needs   : dsi's oid <doc_id>
      --- pagination args : page / per_page 
      --- query args : search_for / search_in / only_stats / ...
      >>> returns : dsi data

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
    query_args = query_data_dsi_arguments.parse_args(request)
    page_args  = pagination_arguments.parse_args(request)
    results, response_code	= Query_db_doc (
      ns, 
      models,
      document_type,
      doc_id,
      claims,
      page_args,
      query_args,
      roles_for_complete = ["admin"],
    )

    log.debug("results have been retrieved ... " )
    # log.debug("results : \n%s ", pformat(results) )

    return results, response_code


@ns.route("/get_one_stats/<string:doc_id>")
class Dsi_stats_(Resource):
  
  @ns.doc('dsi_stats')
  # @ns.expect(query_data_stats_arguments)
  @ns.expect( [mod_stats_query], query_data_stats_arguments)
  # @ns.expect({ "stats_query": [mod_stats_query] }, query_data_stats_arguments)
  # @ns.expect( [[mod_stats_query] })
  # @jwt_optional
  @jwt_optional_sd
  @ns.doc(params={'doc_id': 'the dataset input oid'})
  def post(self, doc_id):
    """
    post stat request from a specific dsi in db

    :param doc_id : dsi's oid <doc_id>

    >
      --- needs   : dsi's oid <doc_id>
      --- query args : search_for / search_in / only_stats / ...
      >>> returns : dsi data

    """
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    document_stat_type = "dsi_doc"

    ### check client identity and claims
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    # log.debug("request : \n%s", pformat(request.__dict__) )
    log.debug("request.args : \n%s", pformat(request.args) )

    ### DEBUG check payload
    log.debug ("ns.payload : \n{}".format(pformat(ns.payload)))

    ### query db from generic function 		
    query_args = query_data_stats_arguments.parse_args(request)
    log.debug("query_args : \n%s", pformat(query_args) )

    results, response_code	= Query_db_stats (
      ns, 
      document_type,
      claims,
      query_args,
      doc_id = doc_id,
      is_one_stat = True,
      roles_for_complete = ["admin"],
			payload = ns.payload
    )

    log.debug("stats results have been retrieved ... " )
    log.debug("results : \n%s ", pformat(results) )

    return results, response_code


@ns.route('/list')
class Dsi_List(Resource):

  @ns.doc('dsi_list')
  @ns.expect(query_pag_args)
  # @jwt_optional
  @jwt_optional_sd
  # @anonymous_required
  def get(self):
    """
    list of all dsi in db

    >
      --- needs   : nothing - 
      --- pagination args : page / per_page 
      --- query args : q_title / q_description / tags / oids / only_stats
      >>> returns : projects data as a list

    """

    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    log.debug ("payload : \n{}".format(pformat(ns.payload)))


    ### check client identity and claims
    claims = get_jwt_claims() 
    # claims = returnClaims(is_optional=True)
    log.debug("claims : \n %s", pformat(claims) )


    ### query db from generic function 		
    query_args = query_arguments.parse_args(request)
    page_args  = pagination_arguments.parse_args(request)
    results, response_code	= Query_db_list (
      ns, 
      models,
      document_type,
      claims,
      page_args,
      query_args,
      roles_for_complete = ["admin"],
    )

    log.debug("results have been retrieved ... " )
    # log.debug("results : \n%s ", pformat(results) )
    
    return results, response_code


@ns.route("/list_stats")
class Dsi_list_stats_(Resource):
  
  @ns.doc('dsi_list_stats')
  # @ns.expect(query_data_stats_arguments)
  @ns.expect( [mod_stats_query], query_data_stats_arguments)
  # @ns.expect({ "stats_query": [mod_stats_query] }, query_data_stats_arguments)
  # @ns.expect( [[mod_stats_query] })
  # @jwt_optional
  @jwt_optional_sd
  def post(self):
    """
    post stat request from a list of dsi in db

    >
      --- query args : search_for / search_in / only_stats / ...
      >>> returns : dsi list stats data

    """
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### check client identity and claims
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    # log.debug("request : \n%s", pformat(request.__dict__) )
    log.debug("request.args : \n%s", pformat(request.args) )

    ### DEBUG check payload
    log.debug ("ns.payload : \n{}".format(pformat(ns.payload)))

    ### query db from generic function 		
    query_args = query_data_stats_arguments.parse_args(request)
    log.debug("query_args : \n%s", pformat(query_args) )

    results, response_code	= Query_db_stats (
      ns, 
      document_type,
      claims,
      query_args,
      roles_for_complete = ["admin"],
			payload = ns.payload
    )

    log.debug("stats results have been retrieved ... " )
    log.debug("results : \n%s ", pformat(results) )

    return results, response_code