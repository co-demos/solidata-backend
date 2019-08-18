# -*- encoding: utf-8 -*-

"""
endpoint_dsi_exports.py  
"""

# from flask_csv import send_csv

from solidata_api.api import *

log.debug(">>> api_dataset_inputs ... creating api endpoints for DSI")

from . import api, document_type

### create namespace
ns = Namespace('exports', description='Dataset inputs : export dsi docs')


### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ROUTES
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 


@ns.doc(security='apikey')
@ns.route("/as_csv/<string:doc_id>")
class Dsi_export_csv(Resource):
  
  @ns.doc('dsi_export_csv')
  # @ns.expect(query_arguments)
  # @ns.expect(query_pag_args, query_data_dsi_arguments)
  # @jwt_optional
  @jwt_optional_sd
  # @guest_required 
  @ns.doc(params={'doc_id': 'the dataset input oid'})
  def get(self, doc_id):
    """
    export dsi as csv from a specific dsi oid

    :param doc_id : dsi's oid <doc_id>

    >
      --- needs   : dsi's oid <doc_id>
      >>> returns : dsi data as csv

    """
    ### DEBUGGING
    print()
    print("-+- "*40)
    log.debug( "ROUTE class : %s", self.__class__.__name__ )

    ### check client identity and claims
    claims = returnClaims()
    log.debug("claims : \n %s", pformat(claims) )

    ### query db from generic function 		
    results, response_code	= Query_db_doc_export (
      ns, 
      # models,
      document_type,
      doc_id,
      claims,
      roles_for_complete = ["admin"],
    )

    log.debug("results have been retrieved ... " )

    if response_code != 200 : 
      return results, response_code
    
    else : 

      log.debug("results['ds_data'][0] : \n%s ", pformat(results["ds_data"][0]) )

      ds_filename = results["ds_filename"]
      log.debug("ds_filename : %s ", ds_filename )

      ds_encoding = results["ds_encoding"]
      log.debug("ds_encoding : %s ", ds_encoding )

      ds_delimiter = results["ds_delimiter"]
      log.debug("ds_delimiter : %s ", ds_delimiter )

      ds_data = results["ds_data"]
      log.debug("ds_data[0] : \n%s ", pformat(ds_data[0]) )
      
      ds_cols_to_export = results["ds_cols_to_export"]
      # log.debug("ds_cols_to_export : \n%s ", pformat(ds_cols_to_export) )

      return send_csv(
        ds_data, 
        "{}.csv".format(ds_filename),
        ds_cols_to_export, 
        delimiter=ds_delimiter,
        writer_kwargs={"extrasaction": "ignore"},
        encoding=ds_encoding,
      )

