from django.db import models

# Create your models here.
class Customer(models.Model):
	url = models.CharField(max_length=150)
	short_url = models.CharField(max_length=20, unique=True)
	

	def __str__(self):
		return self.short_url