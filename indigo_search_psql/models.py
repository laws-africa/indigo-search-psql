from django.db import models
from django.contrib.postgres.search import SearchVectorField


class SearchableDocument(models.Model):
    """ Additional model for supporting full text search on an Indigo document.
    """
    document = models.ForeignKey('indigo_api.document', related_name='+', on_delete=models.CASCADE)
    search_text = models.TextField(null=True, blank=True)
    search_vector = SearchVectorField(null=True)

    def update_search_text(self):
        """ Update the `search_text` field with a raw representation of all the text in the document.
        This is used by the `search_vector` field when doing full text search. The `search_vector`
        field is updated from the `search_text` field using a PostgreSQL trigger, installed by
        migration 0032.
        """
        xpath = '|'.join('//a:%s//text()' % c for c in ['coverPage', 'preface', 'preamble', 'body', 'mainBody', 'conclusions'])
        texts = self.doc.root.xpath(xpath, namespaces={'a': self.document.doc.namespace})
        self.search_text = ' '.join(texts)

    @classmethod
    def create_or_update(cls, document):
        """ Create or update the searchable document for this Indigo document.
        """
        searchable, created = cls.objects.get_or_create(document=document)
        searchable.update_search_text()
        searchable.save()

    @classmethod
    def delete_for_document(cls, document):
        """ The document has been soft deleted, delete the search entry.
        """
        searchable = cls.objects.filter(document=document).first()
        if searchable:
            searchable.delete()

