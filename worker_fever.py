from __future__ import absolute_import
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

import django
django.setup()

from django.conf import settings
from grad_cam.utils import log_to_terminal
from grad_cam.models import FEVERJob

import grad_cam.constants as constants
# import PyTorch
# import PyTorchHelpers
from fever_pipeline import FEVERPredict
import pika
import time
import yaml
import json
import traceback
import urllib

# Close the database connection in order to make sure that MYSQL Timeout doesn't occur
django.db.close_old_connections()
fever_predictor = FEVERPredict()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='fever_task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    try:
        print(" [x] Received %r" % body)
        body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value

        log_to_terminal(body['socketid'], {"terminal": "Running... Please wait."})

        result = fever_predictor.predict(body['claim_text'])
        # from IPython import embed; embed(); import os; os._exit(1)
        FEVERJob.objects.create(job_id=body['socketid'],
                                claim_text=body['claim_text'],
                                docids=str(result['docids']),
                                predicted_evidence=str(result['predicted_evidence'].encode('utf-8')),
                                predicted_label = result['predicted_label'])

        # Close the database connection in order to make sure that MYSQL Timeout doesn't occur
        django.db.close_old_connections()

        result['predicted_evidence'] = result['predicted_evidence'].split('@_@')
        result['docids'] = result['docids'].split('@_@')
        # assert len(result['predicted_evidence']) == len(result['docids'])
        result['docids'] = ['https://en.wikipedia.org/wiki/{}'.format(d) for d in result['docids']]

        log_to_terminal(body['socketid'], {"result": json.dumps(result)})
        log_to_terminal(body['socketid'], {"terminal": json.dumps(result)})
        log_to_terminal(body['socketid'], {"terminal": "Completed the FEVER job"})

        ch.basic_ack(delivery_tag = method.delivery_tag)

    except Exception, err:
        log_to_terminal(body['socketid'], {"terminal": json.dumps({"Traceback": str(traceback.print_exc())})})

channel.basic_consume(callback,
                      queue='fever_task_queue')

channel.start_consuming()
