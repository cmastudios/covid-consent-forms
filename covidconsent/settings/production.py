from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['CONSENT_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ['CONSENT_HOSTS'].split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.environ['CONSENT_MYSQL_CONFIG'],
        },
    }
}

CONN_MAX_AGE = int(os.getenv('CONSENT_CONN_AGE', '300'))

# where to store uploaded files, must be writable
MEDIA_URL = 'https://s3-us-west-2.amazonaws.com/consentformmedia.innovationdx.com/'
MEDIAFILE_STORAGE = 'consent.s3_storage.MediaStorage'

# where to store static files with 'manage.py collectstatic'
STATIC_URL = 'https://s3-us-west-2.amazonaws.com/consentformstatic.innovationdx.com/'
STATICFILES_STORAGE = 'consent.s3_storage.StaticStorage'

# email server settings
EMAIL_HOST = os.getenv('SMTP_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_HOST_USER = os.getenv('SMTP_USERNAME', None)
EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASSWORD', None)
EMAIL_USE_TLS = os.getenv('SMTP_TLS', 'false').lower() in ('true', 'yes', '1')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_FROM', None)
SERVER_EMAIL = os.getenv('EMAIL_FROM', None)
ADMINS = [('Admin', a) for a in os.getenv('EMAIL_ADMINS', '').split(',')]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

