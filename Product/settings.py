"""
Django settings for WIKONOMI project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
# import ctypes


# ctypes.windll.LoadLibrary(r"C:\OSGeo4W64\bin\gdal111.dll") 


# if os.name == 'nt':
#     import platform
#     OSGEO4W = r"C:\OSGeo4W"
#     if '64' in platform.architecture()[0]:
#         OSGEO4W +="64"
#     assert os.path.isdir(OSGEO4W),"Directory does not exist: "+OSGEO4W
#     os.environ['OSGEO4W_ROOT'] = OSGEO4W
#     os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
#     os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#     os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7#+*gxkac4+=q0amk$!8-)7e)_kxomsxpf^mtbppzivf(0(#(m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'ckeditor',
    'rest_framework',
    'widget_tweaks',
    'import_export',
    #'gdal20',
    # 'django_comments_xtd',
    # 'django_comments',
    # 'dal',
    # 'dal_select2',
    'bootstrap4',
    'sorl.thumbnail',
    'crispy_forms',
    'crispy_bootstrap5',
    #'django.contrib.gis',
    # 'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Business.apps.BusinessConfig',
    'Product.apps.ProductConfig',
    'Home.apps.HomeConfig',
    'Photo.apps.PhotoConfig',
    'Tag.apps.TagConfig',
    'Profile.apps.ProfileConfig',
    'Comment.apps.CommentConfig',
    'Search.apps.SearchConfig',
    'Follow.apps.FollowConfig',
    'Notification.apps.NotificationConfig',
    'History.apps.HistoryConfig',
    'Budget.apps.BudgetConfig',

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

ROOT_URLCONF = 'WIKONOMI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'file_download')],
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

WSGI_APPLICATION = 'WIKONOMI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # 'NAME': 'wikonomidm', 
        # 'USER': 'postgres', 
        # 'PASSWORD': 'Launch40722',
        # 'HOST': 'local', 
        # 'PORT': '5432',
    }
}

#GDAL_LIBRARY_PATH =r'C:\OSGeo4W64\bin\gdal111.dll'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap5'





EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal301.dll'

