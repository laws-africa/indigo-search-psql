# coding=utf-8
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from indigo.plugins import plugins
from indigo_api.models import Country, PublicationDocument, Task, Work, Workflow, Document
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

        documents = Document.objects.published().filter(work__country=country).order_by('-pk')

        for doc in documents:
            self.stdout.write(self.style.NOTICE(f"Indexing document #{doc.pk}"))
            SearchableDocument.create_or_update(doc)
