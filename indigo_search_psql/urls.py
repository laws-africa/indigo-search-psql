from django.urls import path

import indigo_search_psql.views

urlpatterns = [
    path('search/<slug:country>', indigo_search_psql.views.SearchView.as_view(), name='public-search'),
]
