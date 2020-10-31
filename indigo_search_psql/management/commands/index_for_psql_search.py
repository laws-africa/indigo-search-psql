# coding=utf-8
from django.core.management.base import BaseCommand

from indigo_api.models import Country, Document
from indigo_search_psql.models import SearchableDocument


class Command(BaseCommand):
    help = 'Indexes all published documents for full text search.'

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str, help='A two-letter country code, e.g. \'na\' for Namibia')

    def handle(self, *args, **options):
        country = None
        if options.get('country'):
            country = Country.for_code(options.get('country'))
            self.stdout.write(self.style.NOTICE(f"Indexing {country} only"))

        documents = Document.objects.undeleted().published().order_by('-pk')
        if country:
            documents = documents.filter(work__country=country)

        for doc in documents:
            self.stdout.write(self.style.NOTICE(f"Indexing document #{doc.pk}"))
            SearchableDocument.create_or_update(doc)
