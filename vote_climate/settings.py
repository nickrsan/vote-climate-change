# Django settings for vote_climate project.
import os

import sunlight
sunlight.config.API_KEY = 'eecdb06b778f460a8cc140fdcd2b0185'

_current_dir = os.getcwd()

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# import ALL of the connection data
# DATABASES = {}
from connection import *

APPEND_SLASH = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

media_folder = os.path.join(_current_dir,"public","static","media")
MEDIA_ROOT = media_folder

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/static/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
static_main = os.path.join(_current_dir,"public","static")
static_server = os.path.join(_current_dir,"public","static")
static_collected = os.path.join(_current_dir,"public","static","collected")
STATIC_ROOT = static_collected

LESSC = os.path.join(_current_dir,"utils","less","bin","lessc")
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    media_folder,
	static_main,
	static_server,
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2wa@&amp;pzg%bst+3nb)^h^-*w)u7$q4%*y@qbvgn_s0(b4l((8jd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'pipeline.middleware.MinifyHTMLMiddleware',
)

ROOT_URLCONF = 'vote_climate.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'vote_climate.wsgi.application'

templates_dir = os.path.join(_current_dir,'templates')
TEMPLATE_DIRS = (
	templates_dir,
	'C:/Users/Nick/Eclipse/workspace-main/voteclimate/vote_climate/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'voteclimate',
	'django.contrib.flatpages',
	#'pipeline',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SITE_NAME = "Vote Climate Change"

PIPELINE_CSS = {
	'index': {
		'source_filenames': (
			'public/static/css/foundation.min.css',
			'public/static/css/app.css',
			'public/static/css/jui-start/jquery-ui-1.8.24.custom.css',
			'public/static/css/index_base.css',
			),
		'output_filename': 'css/index.css',
		'extra_context': {
			'media': 'screen,projection',
			},
		},
	}

PIPELINE_JS = {
	'index': {
		'source_filenames': (
			'public/static/js/modernizr.foundation.js',
			'public/static/js/jquery-1.8.2.min.js',
			'public/static/js/jquery.placeholder.js',
			'public/static/js/jquery.foundation.orbit.js',
			'public/static/js/jquery.backstretch.min.js',
			'public/static/js/app.js',
			'public/static/js/jquery-ui-1.8.24.custom.min.js',
			'public/static/js/filedrop-min.js',
			'public/static/js/index_base.js',

			),
		'output_filename': 'js/index.js',
		}
}

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'


twitter_consumer_key = 'pavcG3CaomhAeq6caqWpdg'
twitter_consumer_secret = 'MQUZgPGrj9GIEQ6tlJHrPPMvxhxOHbqgMOJUMUT2m0'
twitter_access_token_key = '884550516-GK5jd3tnPA6Nzow0Cr5hIXLoHb93R4QFm8vWCNnU'
twitter_access_token_secret = 'NUKePC99baGCC4vf1dmeW01wIzPBcXfSbe5qZda3vRc'

AUTOTWEET = True