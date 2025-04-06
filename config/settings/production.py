from .base import *


DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']



# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',  # Название БД
        'USER': 'myuser',  # Имя пользователя
        'PASSWORD': 'mypassword',  # Пароль
        'HOST': 'localhost',  # Если база на этом же сервере
        'PORT': '5432',  # Стандартный порт PostgreSQL
    }
}


# Email
# ADMINS = [('Admin', 'admin@example.com')]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'


CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000",]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
