# -*- encoding: utf-8 -*-

"""
endpoint_dso.py  
"""

from solidata_api.api import *

log.debug(">>> api_dataset_outputs ... creating api endpoints for DSO")

from . import api, document_type

### create namespace
ns = Namespace('infos', description='Dataset outputs : request and list all dso infos')

### import models 
from solidata_api._models.models_dataset_output import * 
mod_doc             = Dso_infos(ns)
model_doc_out       = mod_doc.mod_complete_out
model_doc_guest_out	= mod_doc.model_guest_out
model_doc_min       = mod_doc.model_minimum
models = {
  "model_doc_out"       : model_doc_out ,
  "model_doc_guest_out" : model_doc_guest_out ,
  "model_doc_min"       : model_doc_min ,
} 

from solidata_api._models.models_stats import *
mod_stats       = Stats_query(ns, document_type)
mod_stats_query = mod_stats.model_stats_query

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 





@ns.doc(security='apikey')
@ns.route("/get_one/<string:doc_id>")
class Dso_infos_(Resource):
  
  """
  DSO infos
  GET    - Shows a document's infos 
  """

  @ns.doc('dso_infos')
  @ns.expect(query_pag_args, query_data_dso_arguments)
  # @jwt_optional
  @jwt_optional_sd
  @ns.doc(params={'doc_id': 'the dataset output oid'})
  def get(self, doc_id):
    """
    get infos of a specific dso in db

    :param doc_id : dsi's oid <doc_id>

    >
      --- needs : a dso/project doc_id in the url
      --- optional : request arguments (pagination|query), json web token in headers...  (cf : solidata_api._parsers.parser_classes)
      >>> returns : dso/project data

    """

    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### DEBUG check
    # log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### check client identity and claims
    # claims = get_jwt_claims() 
    claims = returnClaims(is_optional=True)
    log.debug("claims : \n %s", pformat(claims) )


    ### query db from generic function 		
    query_args = query_data_dso_arguments.parse_args(request)
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

    # log.debug("results['data']['infos']['title'] : %s", results['data']['infos']['title']) 
    # log.debug("len(results['data']['data_raw']['f_data']) : %s", len(results['data']['data_raw']['f_data']) )

    return results, response_code


@ns.doc(security='apikey')
@ns.route("/get_one_stats/<string:doc_id>")
class Dso_stats_(Resource):
  
  @ns.doc('dso_stats')
  @ns.expect( [mod_stats_query], query_data_stats_arguments)
  # @jwt_optional
  @jwt_optional_sd
  @ns.doc(params={'doc_id': 'the dataset input oid'})
  def post(self, doc_id):
    """
    post stat request from a specific dso in db

    :param doc_id : dsi's oid <doc_id>

    >
      --- needs   : dso's oid <doc_id>
      --- query args : search_for / only_stats / ...
      >>> returns : dso stats

    """
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    document_stat_type = "dso_doc"

    ### check client identity and claims
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    # log.debug("request : \n%s", pformat(request.__dict__) )
    log.debug("request.args : \n%s", pformat(request.args) )

    ### DEBUG check payload
    log.debug ("payload : \n{}".format(pformat(ns.payload)))

    ### query db from generic function 		
    query_args = query_data_stats_arguments.parse_args(request)
    log.debug("query_args : \n%s", pformat(query_args) )

    stats_results = {
      "msg" : "Dear user, here comes the several series you requested on this document...",
      "query" : query_args,
      "series" : []
    }
    stats_response_code = 200

    for payload_req in ns.payload : 
      results, response_code	= Query_db_stats (
        ns, 
        document_type,
        claims,
        query_args,
        doc_id = doc_id,
        is_one_stat = True,
        roles_for_complete = ["admin"],
        payload = payload_req["agg_fields"]
      )
      log.debug("stats results have been retrieved ... " )
      log.debug("results : \n%s ", pformat(results) )
      stats_results["series"].append({
        "serie_id" : payload_req["serie_id"],
        "results" : results,
      })

    log.debug ("stats_results : \n%s", pformat(stats_results) )
    # return results, response_code
    return stats_results, stats_response_code


@ns.doc(security='apikey')
@ns.route('/list')
class Dso_List(Resource):

  @ns.doc('dso_list')
  @ns.expect(query_pag_args)
  # @jwt_optional
  @jwt_optional_sd
  # @anonymous_required
  def get(self):
    """
    list of all dso in db

    >
      --- needs   : nothing 
      --- optionnal args : pagination, list of oid_prj, list of tags, query...
      >>> returns : dso/prj data as a list

    """

    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )
    log.debug( "request : \n%s", pformat(request.__dict__) )


    ### DEBUG check
    log.debug ("payload : \n{}".format(pformat(ns.payload)))


    ### check client identity and claims
    # claims = get_jwt_claims() 
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    # log.debug("request.args : %s ", request.args)
    # args_type = type(request.__dict__["args"])
    # log.debug("args_type : %s ", args_type)

    ### query db from generic function 		
    query_args				= query_arguments.parse_args(request)
    page_args				= pagination_arguments.parse_args(request)
    log.debug ("page_args : \n{}".format(page_args))

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


@ns.doc(security='apikey')
@ns.route("/list_stats")
class Dso_list_stats_(Resource):
  
  @ns.doc('dso_list_stats')
  # @ns.expect(query_data_stats_arguments)
  @ns.expect( [mod_stats_query], query_data_stats_arguments)
  # @ns.expect({ "stats_query": [mod_stats_query] }, query_data_stats_arguments)
  # @ns.expect( [[mod_stats_query] })
  # @jwt_optional
  @jwt_optional_sd
  def post(self):
    """
    post stat request from a list of dso in db

    >
      --- query args : search_for / only_stats / ...
      >>> returns : dso list stats data

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