from django.conf import settings
from django.urls import re_path

import indigo_search_psql.content_api.v2.views as views

if settings.INDIGO_CONTENT_API_VERSIONED:
    urlpatterns = [
        re_path(r'^v2/search/(?P<country>[a-z]{2})$', views.PublishedDocumentSearchView.as_view(), name='public-search'),
    ]
else:
    urlpatterns = [
        re_path(r'^search/(?P<country>[a-z]{2})$', views.PublishedDocumentSearchView.as_view(), name='public-search'),
    ]
