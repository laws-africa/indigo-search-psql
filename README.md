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

Include the URLs in your `urls.py` after the indigo URLS:

```python
urlpatterns = [
    path('', include('indigo.urls')),
    path('api/', include('indigo_search_psql.urls')),
]
```

Run migrations to setup the database:

```
python manage.py migrate indigo_search_psql
```

And finally re-index all existing documents. This only needs to be done once. After this, updated documents
are re-indexed automatically.

```
python manage.py index_for_psql_search
```

## URLs

This adds a new URL to the API:

    GET /api/v2/search/<country>?q=<search-term>

* Where `<country>` is a two-letter country code
* Parameter ``q``: the search string
* Content types: JSON

This API searches for works in a country. It returns all works that match the
search term in either their title or their body.  Results are returned in
search rank order.  Each result also has a numeric ``_rank`` and an HTML
``_snippet`` with highlighted results.

If more than one expression of a particular work matches the search, then only
the most recent matching expression is returned.

## License and Copyright

The project is licensed under a [GNU GPL 3 license](LICENSE).

Indigo is Copyright 2015-2020 AfricanLII.
