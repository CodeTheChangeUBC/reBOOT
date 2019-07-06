import ssl
from decouple import config

# CELERY_BACKEND_TYPE = config('CELERY_BACKEND_TYPE', default='amqp')
# CELERY_ACCEPT_CONTENT = ['json', 'pickle']
# CELERY_BROKER_URL = config('CLOUDAMQP_URL', default='amqp://guest@localhost//')
# CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='rpc')
# CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'pickle'
# BROKER_USE_SSL=True
# BROKER_USE_SSL={
#     'keyfile': config('SSL_CLIENT_KEY', default='dev/ssl/cert/client_key.pem'),
#     'certfile': config('SSL_CLIENT_CERT', default='dev/ssl/cert/client_certificate.pem'),
#     'ca_certs': config('SSL_CA_CERT', default='dev/ssl/cert/ca_certificate.pem'),
#     'cert_reqs': ssl.CERT_REQUIRED
# }

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

# Set SSL config depending on development or production
if config('CLOUDAMQP_URL', default=False):
    broker_use_ssl = True
else:
    BROKER_USE_SSL={
        'keyfile': config('SSL_CLIENT_KEY', default='dev/ssl/cert/client_key.pem'),
        'certfile': config('SSL_CLIENT_CERT', default='dev/ssl/cert/client_certificate.pem'),
        'ca_certs': config('SSL_CA_CERT', default='dev/ssl/cert/ca_certificate.pem'),
        'cert_reqs': ssl.CERT_REQUIRED
    }
