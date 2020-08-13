from django.apps import AppConfig


class IndigoSearchPSQLAppConfig(AppConfig):
    name = 'indigo_search_psql'
    verbose_name = 'Indigo Search PSQL'

    def ready(self):
        import indigo_search_psql.signals  # noqa
