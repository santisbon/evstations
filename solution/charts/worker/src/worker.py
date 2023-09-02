import logging
import utils
import os
import json
from evfinder import EVFinder
import pika
import urllib3
import uuid
import traceback
from tabulate import tabulate
from pathlib import Path

# DEBUG | INFO | WARNING | ERROR | CRITICAL
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

if os.getenv('ENVIRONMENT') == 'k8s':
    MASTO_TOKEN     = Path('/etc/worker-secret-vol/masto.posttoken').read_text()
    QUEUE_HOST      = Path('/etc/worker-config-vol/queue.svc').read_text()
    QUEUE           = Path('/etc/worker-config-vol/queue.queue').read_text()
    MASTO_DOMAIN    = Path('/etc/worker-config-vol/masto.domain').read_text()
    VISIBILITY      = Path('/etc/worker-config-vol/masto.visibility').read_text()
    QUEUE_USER      = Path('/etc/worker-secret-vol/queue.consumeruser').read_text()
    QUEUE_PASSWORD  = Path('/etc/worker-secret-vol/queue.consumerpassword').read_text()

    logging.debug('Mastodon post token starts with: ' + MASTO_TOKEN[:5])
else:
    MASTO_TOKEN = os.getenv('EV_MASTO_TOKEN') 
    QUEUE_HOST = os.getenv('EV_QUEUE_HOST')
    QUEUE = os.getenv('EV_QUEUE')
    MASTO_DOMAIN = os.getenv('EV_MASTO_DOMAIN') 
    VISIBILITY = 'direct'
    QUEUE_USER = os.getenv('EV_QUEUE_USER')
    QUEUE_PASSWORD = os.getenv('EV_QUEUE_PASSWORD')

url = f"https://{MASTO_DOMAIN}/api/v1/statuses"

def send_no_results_message(status, in_reply_to):
    headers = {'Authorization': f"Bearer {MASTO_TOKEN}",
            'Idempotency-Key' : str(uuid.uuid4())
            }
    # public, unlisted, private (followers only), direct (mentioned users only)
    fields = {'status' : status,
        'in_reply_to_id' : in_reply_to,
        'visibility' : 'direct'
        }
    http = urllib3.PoolManager()
    response = http.request('POST', url, headers=headers, fields=fields)

#@deprecated("Use process_task")
def process_message(ch, method, properties, body): 
    try:
        message = json.loads(body)
        query = message.get('query')
        in_reply_to = message.get('status_id')
        account = message.get('account')
        
        
        logging.debug(query)
        finder = EVFinder()
        finder.set_location(query)  

        if hasattr(finder,'zip') and finder.zip:
            station_list = utils.form_list_of_stations(finder.get_stations().get('fuel_stations'))
            logging.debug(station_list)

            if len(station_list) == 0:
                send_no_results_message(f'{account}\nI couldn\'t find any stations nearby. Please try another location.',
                                        in_reply_to)
            else:
                full_list = tabulate(station_list, tablefmt='plain') # plain | simple
                chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)

                for idx, chunk in enumerate(chunks, start=1):
                    status = f'{account}\n{chunk}'
                    logging.debug(f"Chunk {idx}:\n{chunk}\n")
                    
                    headers = {'Authorization': f"Bearer {MASTO_TOKEN}",
                        'Idempotency-Key' : str(uuid.uuid4())
                        }
                
                    fields = {'status' : status,
                        'in_reply_to_id' : in_reply_to,
                        'visibility' : VISIBILITY
                        }

                    http = urllib3.PoolManager()
                    response = http.request('POST', url, headers=headers, fields=fields) 

                    logging.debug(f"Sent chunk {idx}")
                    logging.debug("Response received:")
                    logging.debug(response.data.decode('utf-8'))
        else:
            send_no_results_message(f'{account}\nI couldn\'t narrow down that location to a small enough area. Could you try adding something more specific like a ZIP/postal code, neighborhood, or landmark?',
                                     in_reply_to)
        
        ch.basic_ack(delivery_tag = method.delivery_tag)
        
    except Exception as e:
        logging.error('Error processing worker message.')
        logging.error(e)
        logging.error(traceback.format_exc())

def process_task(ch, method, properties, body):
    try:
        message = json.loads(body)
        query = message.get('query')
        in_reply_to = message.get('status_id')
        account = message.get('account')
        
        logging.debug(query)
        finder = EVFinder()
        formatted_stations = utils.form_list_of_stations(finder.get_stations_nearest(query).get('fuel_stations'))
        logging.debug(formatted_stations)

        if len(formatted_stations) == 0:
            send_no_results_message(f'{account}\nI couldn\'t find any stations nearby. Please try another location.',
                                    in_reply_to)
        else:
            full_list = tabulate(formatted_stations, tablefmt='plain') # plain | simple
            chunks = utils.split_text_into_chunks(finder.title + '\n' + full_list)

            for idx, chunk in enumerate(chunks, start=1):
                status = f'{account}\n{chunk}'
                logging.debug(f"Chunk {idx}:\n{chunk}\n")
                
                headers = {'Authorization': f"Bearer {MASTO_TOKEN}",
                    'Idempotency-Key' : str(uuid.uuid4())
                    }
            
                fields = {'status' : status,
                    'in_reply_to_id' : in_reply_to,
                    'visibility' : VISIBILITY
                    }

                http = urllib3.PoolManager()
                response = http.request('POST', url, headers=headers, fields=fields) 

                logging.debug(f"Sent chunk {idx}")
                logging.debug("Response received:")
                logging.debug(response.data.decode('utf-8'))
                
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except Exception as e:
        logging.error('Error processing worker message.')
        logging.error(e)
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    try:
        credentials = pika.PlainCredentials(QUEUE_USER, QUEUE_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE, durable=False)

        # Tell RabbitMQ not to give more than one message to a worker at a time. In other words, don't dispatch a new message to a worker 
        # until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy.
        # If all the workers are busy, your queue can fill up. Keep an eye on that to add more workers, or use message TTL.
        channel.basic_qos(prefetch_count=1)
        
        channel.basic_consume(queue=QUEUE, on_message_callback=process_task)
        channel.start_consuming()
    except Exception as e:
        logging.error("Error setting up queue worker.")
        logging.error(e)
        connection.close()
