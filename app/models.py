from django.db import models

# Create your models here.
class Customer(models.Model):
	url = models.CharField(max_length=150)
	short_url = models.CharField(max_length=20, unique=True)
	

	def __str__(self):
		return self.short_url
		
		
		
class Ip_address(models.Model):
        date = models.DateField(auto_now_add=True)
        ip = models.CharField(max_length=50)

        def __str__(self):
                return f"{self.ip} on {self.date}"
                

class Link_only_ip_address(models.Model):
	url = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateField(auto_now_add=True)
	ip = models.CharField(max_length=50)

	def __str__(self):
		return f"{self.ip} on {self.date}"
	
	class Meta:
		ordering = ['date']
