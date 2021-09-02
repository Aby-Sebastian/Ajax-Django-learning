from django.test import TestCase
from .models import Customer

# Create your tests here.

class CustomerTestCase(TestCase):
	def setUp(self):
		Customer.objects.create(url="https://docs.djangoproject.com/en/3.2/topics/testing/overview/", short_url="django", total_clicks=10)
		Customer.objects.create(url="https://docs.djangoproject.com/en/3.2/topics/auth/", short_url="testing", total_clicks=100)