import os
import json
from sseclient import SSEClient
import logging
import utils
from pathlib import Path
from publisher import Publisher

# DEBUG | INFO | WARNING | ERROR | CRITICAL
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

if os.getenv('ENVIRONMENT') == 'k8s':
  MASTO_TOKEN     = Path('/etc/watcher-secret-vol/masto.notificationtoken').read_text() # read:statuses + read:notifications
  MASTO_DOMAIN    = Path('/etc/watcher-config-vol/masto.domain').read_text()
  
  logging.debug('Mastodon notifications token starts with: ' + MASTO_TOKEN[:5])
  logging.debug('Mastodon domain from config vol: ' + MASTO_DOMAIN)
else:
  MASTO_TOKEN = os.getenv('EV_MASTO_TOKEN') # read:statuses + read:notifications
  MASTO_DOMAIN = os.getenv('EV_MASTO_DOMAIN') 
  
publisher = Publisher()

if __name__ == '__main__':
  try:
    url = f"https://{MASTO_DOMAIN}/api/v1/streaming/user/notification"
    headers = {'Authorization': f"Bearer {MASTO_TOKEN}"}

    messages = SSEClient(url, headers=headers)
    publisher.start()
    
    for msg in messages:
      try:
        logging.debug(msg)

        query = utils.get_content(str(msg)) 
        status_id = utils.get_status_id(str(msg))
        account = utils.get_account(str(msg))

        body=json.dumps({'query' : query, 
                      'status_id' : status_id,
                      'account' : account})

        if query:
          logging.debug(query)
          publisher.publish(body)
      except Exception as e:
        logging.error("Error processing SSE " + str(msg))
        logging.error(e)
  except Exception as e:
    logging.error("Error setting up the queue watcher.")
    logging.error(e)
    publisher.stop()
  finally:
    publisher.join()
