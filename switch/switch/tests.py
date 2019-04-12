from django.test import TestCase
from django.urls import reverse

class LoginTest(TestCase):

	def test_root_url_goes_to_login_view(self):
		url = reverse("login")
		response = self.client.get('/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('login', response.url)


	def test_random_url_goes_to_login_view(self):
		url = reverse("login")
		response = self.client.get('/dave')

		self.assertEqual(response.status_code, 302)
		self.assertIn('login', response.url)