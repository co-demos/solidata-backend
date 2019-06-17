"""
auth_distant.py  
- creates a token_required decorator
"""

from log_config import log, pprint, pformat
log.debug (">>> _auth ... loading auth_distant ...")

from flask import request, current_app as app, jsonify

def checkJWT(token, token_type, return_resp=False):
  """ 
  authenticate a token 
  sending request to the auth url / service 
  specified in config
  ... doing so to avoid middle man risk when editing
  """

  print (". "*50)

  auth_mode = app.config["AUTH_MODE"]
  log.debug("checkJWT / auth_mode : %s", auth_mode )
