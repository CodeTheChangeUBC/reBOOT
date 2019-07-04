import ssl
from decouple import config

CELERY_BACKEND_TYPE = config('CELERY_BACKEND_TYPE', default='amqp')
CELERY_ACCEPT_CONTENT = ['json','pickle']
CELERY_BROKER_URL = config('CLOUDAMQP_URL', default='amqp://guest@localhost//')
CELERY_RESULT_BACKEND = config('CLOUDAMQP_URL', default='amqp://guest@localhost//')
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
BROKER_USE_SSL={
    'keyfile': config('SSL_CLIENT_KEY', default='dev/ssl/cert/client_key.pem'),
    'certfile': config('SSL_CLIENT_CERT', default='dev/ssl/cert/client_certificate.pem'),
    'ca_certs': config('SSL_CA_CERT', default='dev/ssl/cert/ca_certificate.pem'),
    'cert_reqs': ssl.CERT_REQUIRED
}
