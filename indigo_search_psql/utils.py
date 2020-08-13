from django.contrib.postgres.search import Value, Func, SearchRank
from django.db.models import TextField
from rest_framework.pagination import PageNumberPagination


class SearchPagination(PageNumberPagination):
    page_size = 20


class Headline(Func):
    """ Helper class for using the `ts_headline` postgres function when executing
    search queries.
    """
    function = 'ts_headline'

    def __init__(self, field, query, config=None, options=None, **extra):
        expressions = [field, query]
        if config:
            expressions.insert(0, Value(config))
        if options:
            expressions.append(Value(options))
        extra.setdefault('output_field', TextField())
        super(Headline, self).__init__(*expressions, **extra)


class SearchRankCD(SearchRank):
    # this takes proximity into account
    function = 'ts_rank_cd'
