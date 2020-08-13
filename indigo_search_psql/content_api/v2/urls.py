from django.urls import re_path

import indigo_search_psql.content_api.v2.views as views

urlpatterns = [
    re_path(r'^search/(?P<country>[a-z]{2})$', views.PublishedDocumentSearchView.as_view(), name='public-search'),
]
