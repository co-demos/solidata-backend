# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_doc.py  
"""

import re
import random

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

from log_config import log, pformat
log.debug("... _core.queries_db.query_doc.py ..." )

from  bson.objectid  import ObjectId
from   flask_restplus import  marshal

from   . import db_dict_by_type, Marshaller
from   solidata_api._choices._choices_docs import doc_type_dict

import operator

from .query_utils import * 

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_doc_export (
    ns, 
    document_type,
    doc_id,
    claims,
    roles_for_complete   = ["admin"],
  ):

  ### DEBUGGING
  print()
  print("-+- "*40)
  log.debug( "... Query_db_doc / document_type : %s", document_type )

  ### prepare marshaller 
  # marshaller = Marshaller(ns, models)

  ### default values
  not_filtered = True
  db_collection = db_dict_by_type[document_type]
  document_type_full = doc_type_dict[document_type]
  user_id = user_oid = None
  user_role  = "anonymous"

  ds_filename = "test_export"
  ds_delimiter = ";"
  ds_encoding = "utf-8"
  ds_cols_to_export = []
  document_out = None

  message  = None
  dft_open_level_show = ["open_data"]
  response_code  = 200
  can_export = True

  if claims or claims!={}  :
    user_role = claims["auth"]["role"]
    user_id   = claims["_id"] ### get the oid as str
    if user_role != "anonymous" : 
      user_oid = ObjectId(user_id)
      log.debug("user_oid : %s", user_oid )
      dft_open_level_show += ["commons"]

  ### sum up all query arguments
  query_resume = {
    "document_type"     : document_type,  
    "doc_id"            : doc_id,
    "user_id"           : user_id,
    "user_role"         : user_role,
    "is_member_of_team" : False,
    "is_creator"        : False,
  }

  ### test presence of dsi | dso from db
  if ObjectId.is_valid(doc_id) : 
    doc_oid   = ObjectId(doc_id)
    document = db_collection.find_one( {"_id": doc_oid } )

  else :
    document = None


  ### check user auth levels and switch can_export if not allowed
  if document_type in ['dsi', 'dso'] and document : 

    ### set up export infos 
    ds_filename = document["infos"]["title"] + "_export"
    log.debug('ds_filename : %s', ds_filename ) 

    if document_type == "dsi" : 
      ds_delimiter = document["specs"]["src_sep"]
    log.debug('ds_delimiter : %s', ds_delimiter ) 

    cols_to_export = document["data_raw"]["f_col_headers"]
    log.debug('cols_to_export : %s', pformat(cols_to_export) ) 

    if document_type == "dsi" : 
      ds_cols_to_export = [ col["f_coll_header_text"] for col in cols_to_export]
    elif document_type == "dso" : 
      ds_cols_to_export = [ col["f_title"] for col in cols_to_export]

    log.debug('ds_cols_to_export : %s', pformat(ds_cols_to_export) ) 

    
    ### check doc's specs : public_auth, team...
    doc_open_level_show = document["public_auth"]["open_level_show"]
    log.debug( "doc_open_level_show : %s", doc_open_level_show )

    ### get doc's owner infos
    created_by_oid = document["log"]["created_by"]
    log.debug( "created_by_oid : %s", str(created_by_oid) )

    ### get doc's team infos
    if "team" in document : 
      team_oids = [ t["oid_usr"] for t in document["team"] ]
      log.debug( "team_oids : \n%s", pformat(team_oids) )

    ### marshal out results given user's claims / doc's public_auth / doc's team ... 
    # for admin or members of the team --> complete infos model
    if user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid : 

      log.debug( "... user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

      # flag as member of doc's team
      if user_oid == created_by_oid :
        query_resume["is_creator"] = True

      # flag as member of doc's team
      if user_oid in team_oids :
        query_resume["is_member_of_team"] = True

      message = "dear user, there is the complete {} export you requested ".format(document_type_full)

    # for other users (not in team, not admin, not ds' creator)
    else :
  
      log.debug( "... user_role NOT in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

      if doc_open_level_show in ["commons", "open_data"] : 
      
        ### for anonymous users 
        if user_id == None or user_role == "anonymous" : 

          if doc_open_level_show != "open_data" : 
            can_export = False
            message = "dear user, you don't have the credentials to export this {} with this oid : {}".format(document_type_full, doc_id) 
        
          else : 
            can_export = True
            message = "dear user, there is the complete {} export you requested ".format(document_type_full)

      else : 
        ### unvalid credentials / empty response
        can_export = False
        response_code  = 401
        message = "dear user, you don't have the credentials to export this {} with this oid : {}".format(document_type_full, doc_id) 


    ### query corresponding dsi_doc | dsi_doc as list of dicts and send back to endpoint
    if can_export : 

      ### prepare mongodb query
      db_collection_docs = db_dict_by_type[ document_type + "_doc" ]
      match_field = "oid_" + document_type
      log.debug('match_field : %s', match_field ) 
      
      ### query mongoDB
      cursor = db_collection_docs.find({ match_field : doc_oid })
      document_out = list(cursor)
      log.debug('document_out[0] : \n%s', pformat(document_out[0])) 


  ### no document but valid oid / empty response
  elif ObjectId.is_valid(doc_id) and document == None : 
    message = "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 


  ### wrong document type
  else : 
    response_code  = 400
    
    if document_type not in ['dsi', 'dso'] : 
      message = "dear user, this document_type is not allowed : {}".format(document_type_full) 
    
    if ObjectId.is_valid(doc_id) == False : 
      message = "dear user, this oid is invalid : {}".format(doc_id) 

  log.debug('response_code : %s', response_code)
  log.debug('query_resume : \n%s', pformat(query_resume)) 

  ### return response
  return {

    "msg"               : message,
    "query"             : query_resume,

    "ds_data"           : document_out,
    "ds_filename"       : ds_filename,
    "ds_delimiter"      : ds_delimiter,
    "ds_encoding"       : ds_encoding,
    "ds_cols_to_export" : ds_cols_to_export,
    
  }, response_code