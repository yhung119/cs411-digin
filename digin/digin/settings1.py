"""
Django settings for project digin.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l+rku5yrr+xbk-r(tvzp3&a%41e0%j@qrcki65==qo_crp*2+d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'leads', # new app
    'rest_framework',
    'rest_framework.authtoken',
    # 'frontend',
	'django_mysql',
	'polls',
    'users',
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

ROOT_URLCONF = 'digin.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

AUTH_USER_MODEL = 'users.CustomUser'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'digin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.mysql',
    #    'OPTIONS': {
    #      'read_default_file': './digin/my.cnf',
    #      'charset': 'utf8mb4',
	#	},
	#	
	#	# 'USER' : 'yi',
	#	# 'PASSWORD' : 'password',
	#	# 'NAME' : 'test',
	#	# 'HOST' : 'localhost',
	#	# 'PORT' : '',
	#	# 'OPTIONS':{
	#	# 	'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
	#		
	#	# 	'read_default_file': './digin/my.cnf',
	#	# },
	#	# 'TEST': {
	#	# 	'CHARSET': 'utf8mb4',
	#	# 	'COLLATION': 'utf8mb4_unicode_ci',	
	#	# }
    #    
    #}
	'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
          'read_default_file': './digin/my.cnf',
          'charset': 'utf8mb4',
		},
		# 'USER' : 'root',
		# 'PASSWORD' : '',
		# 'NAME' : 'test1',
		# 'HOST' : 'localhost',
		# 'PORT' : '3306',
		# 'OPTIONS':{
		# 	'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
		# 	'charset': 'utf8mb4',
		# 	'read_default_file': './digin/my.cnf',
		# },
		# 'TEST': {
		# 	'CHARSET': 'utf8mb4',
		# 	'COLLATION': 'utf8mb4_unicode_ci',	
		# }
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
