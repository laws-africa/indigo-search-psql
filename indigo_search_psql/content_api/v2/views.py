from countries_plus.models import Country
from django.contrib.postgres.search import SearchQuery
from django.db.models import F
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from indigo_api.views.documents import SearchView, DocumentViewMixin
from indigo_api.views.misc import DEFAULT_PERMS
from indigo_content_api.v2.serializers import PublishedDocumentSerializer
from indigo_content_api.v2.views import PlaceAPIBase
from indigo_search_psql.utils import SearchRankCD, Headline, SearchPagination


class PublishedDocumentSearchView(PlaceAPIBase, ListAPIView):
    """ Search published documents.
    """
    queryset = DocumentViewMixin.queryset.published()
    serializer_class = PublishedDocumentSerializer
    pagination_class = SearchPagination
    filter_backends = (DjangoFilterBackend,)
    permission_classes = DEFAULT_PERMS + (DjangoModelPermissionsOrAnonReadOnly,)
    filter_fields = {
        'frbr_uri': ['exact', 'startswith'],
    }
    serializer_class = PublishedDocumentSerializer
    scope = 'works'

    def determine_place(self):
        # TODO: this view should support localities, too
        try:
            self.country = Country.for_code(self.kwargs['country'])
        except Country.DoesNotExist:
            raise Http404

        super(PublishedDocumentSearchView, self).determine_place()

    def get_queryset(self):
        return super().get_queryset().filter(work__country=self.country)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        query = SearchQuery(self.request.query_params.get('q'))
        queryset = queryset.filter(search_vector=query)

        if self.scope == 'works':
            # Search for distinct works, which means getting the latest
            # expression of all matching works. To do this, they must
            # be ordered by expression date, which means paginating
            # search results by rank is a problem.
            # So, get all matching expressions, then paginate by re-querying
            # by document id, and order by rank.
            doc_ids = [d.id for d in queryset.latest_expression().only('id').prefetch_related(None)]
            queryset = queryset.filter(id__in=doc_ids)

        # the most expensive part of the search is the snippet/headline generation, which
        # doesn't use the search vector. It adds about 500ms to the query. Doing it here,
        # or doing it only on the required document ids, doesn't seem to have an impact.
        queryset = queryset \
            .annotate(
            rank=SearchRankCD(F('search_vector'), query),
            snippet=Headline(F('search_text'), query, options='StartSel=<mark>, StopSel=</mark>')) \
            .order_by('-rank')

        return queryset

    def get_serializer(self, queryset, *args, **kwargs):
        serializer = super().get_serializer(queryset, *args, **kwargs)

        # add _rank and _snippet to the serialized docs
        for i, doc in enumerate(queryset):
            serializer.data[i]['_rank'] = doc.rank
            serializer.data[i]['_snippet'] = doc.snippet

        return serializer
