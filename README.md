# indigo-search-psql

This is a plugin for [Indigo](https://github.com/laws-africa/indigo) that adds a search API to the published document
API, based on PostgreSQL's vector search fields. It is a quick-and-easy way of supporting full-text search.

The API is available by default at `/api/v2/search/<country>`.

## Usage

Install with `pip install git+https://github.com/laws-africa/indigo-search-psql.git#egg=indigo-search-psql`.

Add `indigo_search_psql` to your `INSTALLED_APPS` setting in your `settings.py` file, above `indigo`:

```python
INSTALLED_APPS = [
    'indigo_search_psql',
    'indigo',
    ...
]
```

Include the URLs in your `urls.py`:

```python
urlpatterns = [
    path('api/', include('indigo_search_psql.urls')),
    path('', include('indigo.urls')),
]
```
