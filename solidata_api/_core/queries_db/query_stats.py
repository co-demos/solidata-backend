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

from  bson.objectid   import ObjectId
from   flask_restplus   import  marshal

from   . import db_dict_by_type, Marshaller
from   solidata_api._choices._choices_docs import doc_type_dict

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
    is_one_stat = False,
    roles_for_complete   = ["admin"],
    payload = {}
  ):

  ### DEBUGGING
  print()
  print("-+- "*40)
  log.debug( "... Query_db_stats / document_type : %s", document_type )
  # log.debug( "... Query_db_stats / db_dict_by_type : \n%s", pformat(db_dict_by_type) )
  # log.debug( "... Query_db_stats / doc_type_dict : \n%s", pformat(doc_type_dict) )

  ### prepare marshaller 
  # marshaller = Marshaller(ns, models)

  ### default values
  # not_filtered = True
  db_collection = db_dict_by_type[document_type]
  document_type_full = doc_type_dict[document_type]
  user_id = user_oid = None
  user_role  = "anonymous"
  document_out = None
  message  = "testing stats endpoint for the whole app"
  dft_open_level_show = ["open_data"]
  response_code  = 200
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
    "document_type" : document_type,  
    "doc_id"        : doc_id,
    "user_id"       : user_id,
    "user_role"     : user_role,
    "query_args"    : query_args,
    "payload"       : payload,
    "is_member_of_team" : False,
    "is_creator"    : False,
  }

  ### get query arguments
  log.debug('query_args : \n%s', pformat(query_args) )  

  # stats_type_ds = ['dso', 'dsi']
  # stats_type_ds_doc = ['dso_doc', 'dsi_doc']
  # stats_type_coll = ['usr', 'dmt', 'dmf', 'prj', 'tag']


  ### get query arguments
  search_for = query_args.get('search_for', None )
  search_in = query_args.get('search_in', None )
  search_filters = query_args.get('search_filters', None )
  descending = query_args.get('descending', False )
  if descending : 
    sort_order = -1
  else : 
    sort_order = 1

  ### get payload 
  log.debug('payload : \n%s', pformat(payload) )  

  ### starting dict for matching parrt of aggregation
  q_match = { "$match" : {} }

  ### build basic info for db query
  if is_one_stat and doc_id and ObjectId.is_valid(doc_id) : 
    doc_oid   = ObjectId(doc_id)
    document = db_collection.find_one( {"_id": doc_oid })

    db_collection = db_dict_by_type[ document_type + "_doc" ]
    match_field = "oid_" + document_type
    q_match["$match"][match_field] = ObjectId(doc_id)

  elif is_one_stat == False :
    document = db_collection.find({})

  else :
    response_code  = 400
    document = None


  ### start 
  if document : 

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

    

    ### AGGREGATION ###
    ### - - - - - - ### 

    ### build query pipelines for stats

    # $ aggregation
    q_aggregate = []

    # $ matching
    log.debug( "q_match : \n%s", pformat(q_match) )
    if search_for != None and search_for != [] and search_for != [''] :
      search_words = [ "\""+word+"\"" for word in search_for ]
      q_match["$match"]["$text"] = { 
        "$search" : u" ".join(search_words) 
      }
    q_match["$match"] = append_filters_to_query( q_match["$match"], search_filters)
    log.debug( "q_match : \n%s", pformat(q_match) )
    
    q_aggregate.append(q_match)
    
    # $ grouping x payload
    # payload_sorted = sorted(payload, key=lambda i:i["agg_level_group"])
    q_complex_stat = len(payload) > 1
    q_sorting = []

    # $ unwind - loop payload looking for unwindders
    q_unwindders = [] 
    for p in payload : 
      field = p["agg_field"]
      needs_unwind = p["agg_needs_unwind"]
      unwind_separator = p["agg_unwind_separator"]
      if needs_unwind : 
        q_unwindders = [
          { "$addFields": { 
              field : { 
                "$filter" : {
                    "input": { 
                      "$split": [
                        "${}".format(field), unwind_separator
                      ]  
                    },
                    "as": "str",
                    "cond": { "$ne" : [ "$$str", "" ] }
                }
              }
            }},
          { "$unwind" : "${}".format(field) }
        ]
    
    ### $ unwind - append unwindders to aggregation pipelinne
    log.debug( "unwindders : \n%s", pformat(q_unwindders) )
    if len(q_unwindders) > 0 : 
      q_aggregate += q_unwindders

    # $ grouping simple
    if q_complex_stat == False : 

      q_group_block = { 
        "$group" : {
          "_id" : "${}".format( payload[0]["agg_field"] ),
          "count" : { "$sum": 1 }
        }
      }
      q_sort = { 
        "$sort" : { "count" : sort_order } 
      }
    
      q_aggregate.append(q_group_block)
      q_sorting.append(q_sort)
  
    # $ grouping complex
    else : 
      field_0 = payload[0]["agg_field"]
      field_1 = payload[1]["agg_field"]

      # basic complex aggregation
      q_group_block = [
      { "$group": {
          "_id": { 
            field_0: "${}".format(field_0), 
            field_1: "${}".format(field_1) 
          }, 
          "count": { "$sum": 1 }
        }
      }]

      q_group_block_1 = [
      { "$group": {
          "_id": "$_id.{}".format(field_0), 
          "subcounts": { 
            "$addToSet": { 
              "tag_name" : "$_id.{}".format(field_1), 
              "tag_code" : field_1,
              "count": "$count" 
            }, 
          }
        }
      }]

      q_group_block += q_group_block_1

      ### append groupers to aggregation pipelinne
      q_aggregate += q_group_block

      q_sorting = [
        { "$sort" : { "count" : sort_order } },
        { "$sort" : { "subcount.count" : sort_order } }
      ]



    ### add sorters to pipeline
    for sorter in q_sorting : 
      q_aggregate.append(sorter)


    ### check and run pipeline
    log.debug( "q_aggregate : \n%s", pformat(q_aggregate) )
    results = db_collection.aggregate(q_aggregate)
    message  = "stats required for this {}".format(document_type_full)
    document_out = list(results)




  else : 
    message  = "this {} doesn't exist".format(document_type_full)
    response_code = 401

  log.debug('query_resume : \n%s', pformat(query_resume)) 


  ### return response
  return {
    "msg"   : message,
    "data"  : document_out,
    "query" : query_resume,
  }, response_code






  """
  ### examples pipeline aggregation stats 


  ### LOCALLY ### 
  ### - - - - ###

  db.getCollection('datasets_outputs_docs').aggregate([
    { $match: { "oid_dso" : ObjectId("5c8942a48626a059decaa34a") } },
    { $group: {
      _id: "$source", 
      count: { $sum: 1 },
      }
    },
    { $sort : { "count" : 1 } }
  ])


  db.getCollection('datasets_inputs_docs').aggregate([
    { $match: { 
      "oid_dsi" : ObjectId("5c891b3c8626a023e4fd61b3") 
      }
    },
    { $group: {
      _id: "$Label", 
      count: {
        $sum: 1
      }
    }},
    { $sort : { "count" : -1 } }
  ])



  ### IN SOLIDATA PROD ###
  ### - - - - - - - -  ###

  ### SIMPLE COUNT
    db.getCollection('datasets_outputs_docs').aggregate([
      { $match: { "oid_dso" : ObjectId("5c89636d328ed70609be03ab") } },
      { $group: {
          _id: "$source", 
          total: { $sum: 1 }
        }
      },
      { $sort : { "count" : 1 }  },
    ])


  ### COMPLEX COUNT / UNIQUES
    db.getCollection('datasets_outputs_docs').aggregate([
      { $match: { "oid_dso": ObjectId("5c89636d328ed70609be03ab") } },
      { $group: {
          _id: { "source": "$source", "ville structure": "$ville structure" } , 
          count: { $sum: 1 }
        }
      },
      { $group: {
          _id: "$_id.source", 
          subcounts: { $addToSet: { "ville structure": "$_id.ville structure", count: "$count" } }, 
          count: { $sum: 1 }
        }
      },
      { $sort : { "count" : -1 }  },
      { $sort : { "subcounts.count" : -1 }  },
    ])


  ### COMPLEX COUNT / COUNT AND UNWIND TAGS

    db.getCollection('datasets_outputs_docs').aggregate([
      { $match: { "oid_dso": ObjectId("5c89636d328ed70609be03ab") } },
      { $addFields: { "coding services" : { 
          $filter: {
            input: { $split: ["$coding services", "-"]  },
            as: "str",
            cond: { $ne : [ "$$str", "" ] }
          }
        }
      }},
      { $unwind : "$coding services" },
      { $group: {
          _id: { "source" : "$source", "coding services": "$coding services" },
          "coding services": { "$push": "$coding services" } , 
          count: { $sum: 1 }
        }
      },
      { $group: {
            "_id": "$_id.source", 
            "subcounts": { $addToSet: { "coding services": "$_id.coding services", "count" : "$count"  } }, 
          }
      },
    { $sort : { "count" : -1 }  },
    { $sort : { "subcounts.count" : -1 }  },
  ])

  db.getCollection('datasets_inputs_docs').aggregate([
      { $match: {
          "oid_dsi": ObjectId("5d1932db8626a086eb308e68"),
          "$text" : { 
              "$search": "château"
          } 
      }},
      { $addFields: { "coding-services" : { 
          $filter: {
            input: { $split: ["$coding-services", "-"]  },
            as: "str",
            cond: { $ne : [ "$$str", "" ] }
          }
        }
      }},
      { $unwind : "$coding-services" },
      { $group: {
          _id: { "sourceur" : "$sourceur", "coding-services": "$coding-services" },
          "coding-services": { $push: "$coding-services" }, 
          count: { $sum: 1 }
      }},
      { $group: {
          _id: "$_id.sourceur", 
            subcounts: { $addToSet: { 
              "tag_name": "$_id.coding-services", 
              "tag_code": "coding-services",                 
              count : "$count"  
            }}, 
      }},
      { $sort : { "subcounts.count" : -1 }  }
  ])


  db.getCollection('datasets_outputs_docs').aggregate([
    { $match: { "oid_dso": ObjectId("5c89636d328ed70609be03ab") } },
    { $addFields: { "coding services" : { 
        $filter: {
          input: { $split: ["$coding services", "-"]  },
          as: "str",
          cond: { $ne : [ "$$str", "" ] }
        }
      }
    }},
    { $unwind : "$coding services" },
    { $group: {
        _id: { "source" : "$source", "coding services": "$coding services" },
        "coding services": { $push: "$coding services" } , 
        count: { $sum: 1 }
      }
    },
    { $group: {
        _id: "$_id.source", 
          subcounts: { $addToSet: { 
            "tag_name": "$_id.coding services", 
            "tag_code": "coding services",                 
            count : "$count"  } }, 
        }
      }
    },
    { $sort : { "subcounts.count" : -1 }  },

  ])


  """ 









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
  #     response_code  = 401
  #     ### unvalid credentials / empty response
  #     message = "dear user, you don't have the credentials to access/see this {} with this oid : {}".format(document_type_full, doc_id) 



  # else : 
  #   ### no document / empty response
  #   response_code = 404
  #   message       = "dear user, there is no {} with this oid : {}".format(document_type_full, doc_id) 
  #   document_out  = None

