import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '0z1z2^oq!w5tz@6cjd^j10q9hzbfq8*t!c0r+&g5uj@gw2=bjn'

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0', 'testserver']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'login',
    'scheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'switch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR+'/switch/templates',
            BASE_DIR+'/login/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'switch.context_processors.from_settings',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'switch.wsgi.application'

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'switch',
        'USER': 'switchuser',
        'PASSWORD': 'switchpass',
        'HOST': 'localhost',
        'PORT': '',
    }
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': '',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

JQUERY_VERSION           = '3.1.1'
JQUERY_JS_LINK           = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/' + JQUERY_VERSION + '/jquery.min.js'

ANGULAR_VERSION          = '1.5.8'
ANGULAR_JS_LINK          = 'https://cdnjs.cloudflare.com/ajax/libs/angular.js/' + ANGULAR_VERSION + '/angular.min.js'

FONT_AWSOME_VERSION      = '4.7.0'
FONT_AWSOME_CSS_LINK     = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/' + FONT_AWSOME_VERSION  + '/css/font-awesome.min.css'

SEMANTIC_VERSION         = '2.4.1' # '2.1.7'
SEMANTIC_CSS_LINK        = 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/' + SEMANTIC_VERSION + '/semantic.min.css'
SEMANTIC_JS_LINK         = 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/' + SEMANTIC_VERSION + '/semantic.min.js'

MARKDOWN_EDITOR_VERSION  = '1.11.2'
MARKDOWN_EDITOR_JS_LINK  = 'https://cdnjs.cloudflare.com/ajax/libs/simplemde/' + MARKDOWN_EDITOR_VERSION + '/simplemde.min.js'
MARKDOWN_EDITOR_CSS_LINK ='https://cdnjs.cloudflare.com/ajax/libs/simplemde/' + MARKDOWN_EDITOR_VERSION + '/simplemde.min.css'

MOMENTJS_VERSION         = '2.18.1'
MOMENTJS_JS_LINK         = 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/' + MOMENTJS_VERSION + '/moment.min.js'

ANGULAR_MOMENTJS_VERSION = '1.0.1'
ANGULAR_MOMENTJS_JS_LINK = 'https://cdnjs.cloudflare.com/ajax/libs/angular-moment/' + ANGULAR_MOMENTJS_VERSION + '/angular-moment.min.js'