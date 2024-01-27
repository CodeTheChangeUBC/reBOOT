import ssl

from decouple import config

broker_url = config('CLOUDAMQP_URL', default='amqp://guest@localhost//')
broker_connection_timeout = 30
broker_heartbeat = None
broker_pool_limit = 1
event_queue_expires = 60
worker_prefetch_multiplier = 1
worker_concurrency = 1
accept_content = ['json', 'pickle']
result_backend = config("REDIS_URL")
task_serializer = 'pickle'
result_serializer = 'pickle'
task_track_started = True
task_ignore_result = False

# Use PROD settings if valid CLOUDAMQP_URl, else dev
if config('CLOUDAMQP_URL', default=False):
    broker_use_ssl = True
else:
    broker_use_ssl = {
        'keyfile': 'dev/ssl/cert/client_key.pem',
        'certfile': 'dev/ssl/cert/client_certificate.pem',
        'ca_certs': 'dev/ssl/cert/ca_certificate.pem',
        'cert_reqs': ssl.CERT_REQUIRED
    }
