from django.db.models import signals
from django.dispatch import receiver

from indigo_api.models import Document
from indigo_search_psql.models import SearchableDocument


@receiver(signals.post_save, sender=Document)
def document_saved(sender, instance, **kwargs):
    if not kwargs['raw']:
        if instance.deleted:
            SearchableDocument.delete_for_document(instance)
        else:
            SearchableDocument.create_or_update(instance)
