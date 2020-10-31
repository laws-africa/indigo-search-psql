# settings for running api tests

from indigo.settings import *

INSTALLED_APPS = ['indigo_search_psql'] + list(INSTALLED_APPS)

# allows us to test permissions
INDIGO_AUTH_REQUIRED = True

ROOT_URLCONF = 'indigo_search_psql.tests.urls'
