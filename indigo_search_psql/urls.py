from django.conf import settings
from django.urls import path, include

from indigo_content_api.urls import APP_NAME


if settings.INDIGO_CONTENT_API_VERSIONED:
    # Versioned API URLs
    urlpatterns = [
        path('v2a/', include(('indigo_search_psql.content_api.v2.urls', APP_NAME), namespace='v2')),
    ]
else:
    # Unversioned API URLs, latest only
    urlpatterns = [
        path('', include(('indigo_search_psql.content_api.v2.urls', APP_NAME), namespace='v2'))
    ]
