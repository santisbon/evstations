import threading
from time import sleep
from pika import ConnectionParameters, BlockingConnection, PlainCredentials, BasicProperties, spec
import logging
import os
from pathlib import Path

if os.getenv('ENVIRONMENT') == 'k8s':
    QUEUE_USER      = Path('/etc/watcher-secret-vol/queue.produceruser').read_text()
    QUEUE_PASSWORD  = Path('/etc/watcher-secret-vol/queue.producerpassword').read_text()
    QUEUE           = Path('/etc/watcher-config-vol/queue.queue').read_text()
    QUEUE_HOST      = Path('/etc/watcher-config-vol/queue.svc').read_text()
else:
    QUEUE_USER = os.getenv('EV_QUEUE_USER')
    QUEUE_PASSWORD = os.getenv('EV_QUEUE_PASSWORD')
    QUEUE = os.getenv('EV_QUEUE')
    QUEUE_HOST = os.getenv('EV_QUEUE_HOST')

class Publisher(threading.Thread):
    """
    Long-running publisher that responds to heartbeats and other data events.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.is_running = True
        self.name = "Publisher"

        credentials = PlainCredentials(QUEUE_USER, QUEUE_PASSWORD)
        parameters = ConnectionParameters(host=QUEUE_HOST, credentials=credentials)
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE, durable=False)

    def run(self):
        while self.is_running:
            self.connection.process_data_events(time_limit=1)

    def _publish(self, message):
        self.channel.basic_publish(exchange='', 
                                   routing_key=QUEUE, 
                                   body=message.encode(),
                                   properties=BasicProperties(delivery_mode=spec.TRANSIENT_DELIVERY_MODE)) # PERSISTENT_DELIVERY_MODE | TRANSIENT_DELIVERY_MODE)

    def publish(self, message):
        self.connection.add_callback_threadsafe(lambda: self._publish(message))

    def stop(self):
        logging.debug("Stopping...")
        self.is_running = False
        # Wait until all the data events have been processed
        self.connection.process_data_events(time_limit=1)
        if self.connection.is_open:
            self.connection.close()
        logging.debug("Stopped")

