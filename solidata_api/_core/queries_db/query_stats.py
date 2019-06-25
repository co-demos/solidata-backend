# -*- encoding: utf-8 -*-

"""
_core/queries_db/query_stats.py  
"""

import re
import random

import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

from log_config import log, pformat
log.debug("... _core.queries_db.query_stats.py ..." )

from	bson.objectid 	import ObjectId
from 	flask_restplus 	import  marshal

from 	. import db_dict_by_type, Marshaller
from 	solidata_api._choices._choices_docs import doc_type_dict

import operator

from .query_utils import * 

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### GLOBAL FUNCTION TO QUERY ONE DOC FROM DB
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### cf : response codes : https://restfulapi.net/http-status-codes/ 

def Query_db_stats (
    ns, 
    document_type,
    claims,
    query_args,
    doc_id = None,
    roles_for_complete 	= ["admin"],
    payload = {}
  ):

  ### DEBUGGING
  print()
  print("-+- "*40)
  log.debug( "... Query_db_stats / document_type : %s", document_type )

  ### prepare marshaller 
  # marshaller = Marshaller(ns, models)

  ### default values
  not_filtered = True
  db_collection = db_dict_by_type[document_type]
  document_type_full = doc_type_dict[document_type]
  user_id = user_oid = None
  user_role	= "anonymous"
  document_out = None
  message	= "testing stats endpoint for the whole app"
  dft_open_level_show = ["open_data"]
  response_code	= 200
  can_access_complete = True

  if claims or claims!={}  :
    user_role = claims["auth"]["role"]
    user_id   = claims["_id"] ### get the oid as str
    if user_role and user_role != "anonymous" : 
      user_oid = ObjectId(user_id)
      log.debug("user_oid : %s", user_oid )
      dft_open_level_show += ["commons"]

  ### sum up all query arguments
  query_resume = {
    "document_type"	: document_type,	
    "doc_id" 				: doc_id,
    "user_id" 			: user_id,
    "user_role"			: user_role,
    "query_args"		: query_args,
    "payload"	      : payload,
    "is_member_of_team" : False,
    "is_creator" 		: False,
  }

  ### get query arguments
  log.debug('query_args : \n%s', pformat(query_args) )  

  stats_type_ds = ['dso', 'dsi']
  stats_type_coll = ['usr', 'dmt', 'dmf', 'prj', 'tag']




  ### TO DO : SEPARATE DSO/DSI and OTHERS for stats rrequest





  ### retrieve from db
  if doc_id and ObjectId.is_valid(doc_id) : 
    doc_oid	 = ObjectId(doc_id)
    # document = db_collection.find_one( {"_id": doc_oid })
  
  else :
    response_code	= 400
    # document = None



  # if document : 

  # ### check doc's specs : public_auth, team...
  # doc_open_level_show = document["public_auth"]["open_level_show"]
  # log.debug( "doc_open_level_show : %s", doc_open_level_show )

  # ### get doc's owner infos
  # created_by_oid = document["log"]["created_by"]
  # log.debug( "created_by_oid : %s", str(created_by_oid) )

  # ### get doc's team infos
  # if "team" in document : 
  #   team_oids = [ t["oid_usr"] for t in document["team"] ]
  #   log.debug( "team_oids : \n%s", pformat(team_oids) )

  # ### marshal out results given user's claims / doc's public_auth / doc's team ... 
  # # for admin or members of the team --> complete infos model
  # if user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid : 

  #   log.debug( "... user_role in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

  #   # flag as member of doc's team
  #   if user_oid == created_by_oid :
  #     query_resume["is_creator"] = True

  #   # flag as member of doc's team
  #   if user_oid in team_oids :
  #     query_resume["is_member_of_team"] = True

  #   document_out = {}

  #   message = "dear user, there is the complete {} you requested ".format(document_type_full)

  # # for other users
  # else :

  #   log.debug( "... user_role NOT in roles_for_complete or user_oid in team_oids or user_oid == created_by_oid " )

  #   if doc_open_level_show in ["commons", "open_data"] : 
    
  #     ### for anonymous users --> minimum infos model
  #     if user_id == None or user_role == "anonymous" : 
  #       document_out = {}

      
  #     ### for registred users (guests) --> guest infos model
  #     else :
  #       document_out = {}
      


  #     message = "dear user, there is the {} you requested given your credentials".format(document_type_full)

  #   else : 
  #     response_code	= 401
  #     ### unvalid credentials / empty response
  #     message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 



  # else : 
  #   ### no document / empty response
  #   response_code = 404
  #   message       = "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 
  #   document_out  = None


  log.debug('query_resume : \n%s', pformat(query_resume)) 


  ### return response
  return {
    "msg" 	  : message,
    "data"	  : document_out,
    "query"	  : query_resume,
  }, response_code