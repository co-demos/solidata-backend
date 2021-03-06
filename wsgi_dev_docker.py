import os 
from log_config import log, pformat

from solidata_api.application import create_app

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### ENV VARS
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path_global = Path('.') / 'example.env.global'
load_dotenv(env_path_global, verbose=True)

### overide env vars for Docker
os.environ["DOCKER_MODE"]   = 'docker_on'

### READ ENV VARS
run=os.getenv('RUN_MODE', 'dev')
docker=os.getenv('DOCKER_MODE', 'docker_off')
mongodb=os.getenv('MONGODB_MODE', 'local')

auth_mode=os.getenv('AUTH_MODE', 'internal')

RSA=os.getenv('RSA_MODE', False)
anojwt=os.getenv('ANOJWT_MODE', False)
antispam=os.getenv('ANTISPAM_MODE', False)
antispam_val=os.getenv('ANTISPAM_VAL', 'my-string-to-check')


### READ ENV VARS DEPENDING ON MODE

# MONGODB - RELATED 
if mongodb in ['local'] : 
  env_path_mongodb = Path('.') / 'example.env.mongodb'
else : 
  env_path_mongodb = Path('.') / '.env.mongodb'

# MAILING - RELATED 
if run == 'dev_email' : 
  env_path_mailing = Path('.') / '.env.mailing'
else : 
  env_path_mailing = Path('.') / 'example.env.mailing'

if auth_mode != 'internal' : 
  env_path_auth = Path('.') / '.env.auth'
else : 
  env_path_auth = Path('.') / 'example.env.auth'

load_dotenv(env_path_mongodb, verbose=True)
load_dotenv(env_path_mailing, verbose=True)
load_dotenv(env_path_auth, verbose=True)

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
### FLASK-SOCKETIO
### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###
from flask_socketio import SocketIO

### + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ###

app = create_app( 
  app_name='SOLIDATA_API_DEV_DOCKER', 

  run_mode=run, 
  docker_mode=docker,
  mongodb_mode=mongodb,
  
  auth_mode=auth_mode,

  RSA_mode=RSA,
  anojwt_mode=anojwt,
  antispam_mode=antispam,
  antispam_value=antispam_val,
)

### initiate socketio
socketio = SocketIO(app)

if __name__ == "main" :
    
  log.debug("\n--- STARTING AUTH API (PROD) ---\n")
  
  # app.run()
  app.run(host='0.0.0.0', port=4000)