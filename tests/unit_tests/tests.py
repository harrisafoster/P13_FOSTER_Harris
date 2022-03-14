from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')

    def test_get_index(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

    def test_template_index(self):
        response = self.client.get(self.index_url)
        self.assertTemplateUsed(response, 'index.html')

    def test_title_index(self):
        response = self.client.get(self.index_url)
        self.assertIn(b'Holiday Homes', response.content)
