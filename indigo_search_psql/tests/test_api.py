from django.test.utils import override_settings
from sass_processor.processor import SassProcessor
from rest_framework.test import APITestCase

# Ensure the processor runs during tests. It doesn't run when DEBUG=False (ie. during testing),
# but during testing we haven't compiled assets
SassProcessor.processor_enabled = True


# Disable pipeline storage - see https://github.com/cyberdelia/django-pipeline/issues/277
@override_settings(STATICFILES_STORAGE='pipeline.storage.PipelineStorage', PIPELINE_ENABLED=False)
class SearchTest(APITestCase):
    api_path = '/v2'
    api_host = 'testserver'
    fixtures = ['languages_data', 'countries', 'user', 'editor', 'taxonomies', 'work', 'published', 'colophon',
                'attachments', 'commencements']

    def setUp(self):
        self.client.login(username='api-user@example.com', password='password')

    def test_published_search_perms(self):
        self.client.logout()
        response = self.client.get(self.api_path + '/search/za?q=act')
        self.assertEqual(response.status_code, 403)

    def test_published_search(self):
        response = self.client.get(self.api_path + '/search/za?q=act')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
