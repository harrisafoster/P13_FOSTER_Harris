from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_profiles_index = reverse('profiles_index')

        self.user_object = User.objects.create(username='testuser', password='PDX1337!')
        self.profile_object = Profile.objects.create(user=self.user_object,
                                                     favorite_city='Portland')
        self.url_profile = reverse('profile', args=[self.user_object.username])

    def test_get_profiles_index(self):
        response = self.client.get(self.url_profiles_index)
        self.assertEqual(response.status_code, 200)

    def test_template_profiles_index(self):
        response = self.client.get(self.url_profiles_index)
        self.assertTemplateUsed(response, 'profiles/index.html')

    def test_title_profiles_index(self):
        response = self.client.get(self.url_profiles_index)
        self.assertIn(b'Profiles', response.content)

    def test_get_one_profile(self):
        response = self.client.get(self.url_profile)
        self.assertEqual(response.status_code, 200)

    def test_template_one_profile(self):
        response = self.client.get(self.url_profile)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_title_one_profile(self):
        response = self.client.get(self.url_profile)
        self.assertIn(b'testuser', response.content)
