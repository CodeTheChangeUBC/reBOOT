import ssl
from decouple import config


broker_url = config('CLOUDAMQP_URL', default='amqp://guest@localhost//')
broker_pool_limit = 1
broker_heartbeat = None
broker_connection_timeout = 30
broker_use_ssl = True
event_queue_expires = 60
result_backend = 'rpc'
worker_prefetch_multiplier = 1
worker_concurrency = 10
task_serializer = 'pickle'
result_serializer = 'pickle'
accept_content = ['json', 'pickle']

# Use prod if valid CLOUDAMQP_URl, else dev
if config('CLOUDAMQP_URL', default=False):
    broker_use_ssl = True
else:
    BROKER_USE_SSL = {
        'keyfile': 'dev/ssl/cert/client_key.pem',
        'certfile': 'dev/ssl/cert/client_certificate.pem',
        'ca_certs': 'dev/ssl/cert/ca_certificate.pem',
        'cert_reqs': ssl.CERT_REQUIRED
    }
