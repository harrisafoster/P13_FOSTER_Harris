from django.test import Client, TestCase
from django.urls import reverse
from .models import Address, Letting


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.address_object = Address.objects.create(
            number='4',
            street='Military Street',
            city='Willoughby',
            state='OH',
            zip_code='44094',
            country_iso_code='USA',
        )
        self.letting_object = Letting.objects.create(title='TestTitle',
                                                     address=self.address_object)
        self.url_lettings_index = reverse('lettings_index')
        self.url_letting = reverse('letting', args=[self.letting_object.id])

    def test_get_lettings_index(self):
        response = self.client.get(self.url_lettings_index)
        self.assertEqual(response.status_code, 200)

    def test_template_lettings_index(self):
        response = self.client.get(self.url_lettings_index)
        self.assertTemplateUsed(response, 'lettings/index.html')

    def test_title_lettings_index(self):
        response = self.client.get(self.url_lettings_index)
        self.assertIn(b'Lettings', response.content)

    def test_get_one_letting(self):
        response = self.client.get(self.url_letting)
        self.assertEqual(response.status_code, 200)

    def test_template_one_letting(self):
        response = self.client.get(self.url_letting)
        self.assertTemplateUsed(response, 'lettings/letting.html')

    def test_title_one_letting(self):
        response = self.client.get(self.url_letting)
        self.assertIn(b'TestTitle', response.content)
