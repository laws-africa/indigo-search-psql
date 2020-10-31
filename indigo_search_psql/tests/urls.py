# URLs for api tests

from django.urls import include, path

urlpatterns = [
    path('', include('indigo_content_api.urls')),
    path('', include('indigo_search_psql.urls')),
]
