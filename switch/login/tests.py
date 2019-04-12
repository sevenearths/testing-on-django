from django.test import TestCase
from django.urls import reverse

class LoginTest(TestCase):

	def test_login_view(self):
		url = reverse("login")
		resp = self.client.get(url)

		self.assertEqual(resp.status_code, 200)
		self.assertIn('Login', resp.content.decode('utf-8'))