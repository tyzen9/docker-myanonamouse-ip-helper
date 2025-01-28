import os
import sys
import json
import time
import datetime
import logging
from colorlog import ColoredFormatter

###########################################
# Process environment variables
###########################################

# MAM_ID is required to be in the environment, if not throw an error
MANDATORY_ENV_VARS = ['MAM_ID']
for var in MANDATORY_ENV_VARS:
    if var not in os.environ:
        raise EnvironmentError("Failed because mandatory environment variable(s) {} is not set.".format(var))
MAM_ID = os.environ.get('MAM_ID')

# Calls are only permitted once an hour, this can be tweaked using the UPDATE_INTERVAL env variable
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', '3600'))

# Determine the log level to be used, the default will be INFO
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
if LOG_LEVEL not in ['DEBUG','INFO','WARNING','ERROR','CRITICAL']:
    LOG_LEVEL = 'INFO'

###########################################
# Setup Logging
###########################################
# Create a logger
#logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger()
loglevel = logging.getLevelName(LOG_LEVEL)
logger.setLevel(loglevel)

# Create formatter and add it to the handler
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG':    'light_black',
        'INFO':     'white',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Create a stream handler for formatting, and initiate the format
handler = logging.StreamHandler()
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)

###########################################
# Functions
###########################################

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def splashLogo():
    """
    Print the splash screen to the logs
    """
    logging.info(f'''
 _____                                                          _____ 
( ___ )                                                        ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   |                                                          |   | 
 |   |   ████████╗██╗   ██╗███████╗███████╗███╗   ██╗ █████╗    |   | 
 |   |   ╚══██╔══╝╚██╗ ██╔╝╚══███╔╝██╔════╝████╗  ██║██╔══██╗   |   | 
 |   |      ██║    ╚████╔╝   ███╔╝ █████╗  ██╔██╗ ██║╚██████║   |   | 
 |   |      ██║     ╚██╔╝   ███╔╝  ██╔══╝  ██║╚██╗██║ ╚═══██║   |   | 
 |   |      ██║      ██║   ███████╗███████╗██║ ╚████║ █████╔╝   |   | 
 |   |      ╚═╝      ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚════╝    |   | 
 |   |                https://github.com/tyzen9                 |   | 
 |   |                    Made in the U.S.A.                    |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                        (_____)

''')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():
    # Wait one minute to make sure networking is established.

    # The mam_id is pretty big, lets make sure it has some meat to it.
    if (len(MAM_ID) < 25):
        logging.error(f'A valid \'MAM_ID\' environment value must be set, see https://www.myanonamouse.net/preferences/index.php?view=security for more info.')
        sys.exit('Invalid MAM_ID');

    logging.info(f'MAM seedbox updates will begin in one minute, continuing every {UPDATE_INTERVAL} seconds thereafter.')
    time.sleep(60)
    while True:
        logging.info(f'---------------------------------------------------------')
        # Get the current IP address for logging purposes only
        ip_address = os.popen('curl --silent http://ipinfo.io/ip').read()

        # This is the call we will make to set the myanonamouse seedbox IP using the required MAM_ID
        logging.info(f'Attempting to update myanonamouse seedbox...')
        seedbox_call = 'curl --silent -c ~/mam.cookies -b \'mam_id='+MAM_ID+'\' https://t.myanonamouse.net/json/dynamicSeedbox.php'
        logging.debug(f'\t URL: {seedbox_call}')
        # Make the call and analyze the result
        mam_response = os.popen(seedbox_call).read()
        mam_result = json.loads(mam_response);
        logging.debug(f'\t RESULT: {mam_response} SUCCESS: {mam_result['Success']}')

        # If the the call was a success
        if (mam_result['Success']):
            logging.info(f'SUCCESS - Result: {mam_result['msg']}')
            logging.info(f'\t Your myanonamouse seedbox accepts connections from: {ip_address}')
        # Otherwise...
        else:
            logging.error(f'Unable to update seedbox: {mam_result['msg']}')

        # Wait the set amount of time, and try updating again
        logging.info(f'---------------------------------------------------------')
        logging.info(f'Attempt another update in {UPDATE_INTERVAL} seconds')
        time.sleep(UPDATE_INTERVAL)

###########################################
# Main
###########################################

# Was this script called directly?  Then lets go....
if __name__=="__main__": 
    splashLogo()
    main()