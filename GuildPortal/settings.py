"""
Django settings for GuildPortal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ih93h%7&1d3sujq!m3zwgp%=bs!7*+t1k9%(+dma5+fo%ii%o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'sslserver',
    # 'usersettings',
    'guardian',
    'debug_toolbar',
    'account',
    'PortalAdmin',
    'SuperPortal',
    'Portal',
    'PortalEnrollment',
    'Forum',
    'PortalMessaging',
    'PortalRaid',
    'pinax_theme_bootstrap'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader'
)


ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'guardian.backends.ObjectPermissionBackend',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'GuildPortal.middlewares.ProfilerMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',

)

ROOT_URLCONF = 'GuildPortal.urls'
SITE_ID = 1
# USERSETTINGS_MODEL='SuperPortal.GuildSettings'
WSGI_APPLICATION = 'GuildPortal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "mydb",
        'USER': 'portal_admin',
        'PASSWORD': 'caca04',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = False

ugettext = lambda s: s
LANGUAGES = (
    ('fr', ugettext('French')),
)
FORUMS_EDIT_TIMEOUT = 120

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.getcwd(), 'media/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'GuildPortal.ContextProcessor.menu.menu',
                'account.context_processors.account',
                'GuildPortal.ContextProcessor.menu.guild_info',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'pinax_theme_bootstrap.context_processors.theme'

            ],
        },
    }
]

# STATICFILES_DIRS = (
#     MEDIA_ROOT,
# )


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)