from django.db import models

# Create your models here.
class Customer(models.Model):
	url = models.CharField(max_length=150)
	short_url = models.CharField(max_length=20, unique=True)
	count=models.IntegerField(default=0,blank=True, null=True)

	def __str__(self):
		return self.short_url
	
	def increment_count(self):
		self.count+=1
		return self.count

		
class Ip_address(models.Model):
    date = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=50)

    def __str__(self):
            return f"{self.ip} on {self.date}"

    class Meta:
    	ordering = ['-date']
                

class Link_only_ip_address(models.Model):
	url = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	ip = models.CharField(max_length=50)
	device = models.CharField(max_length=100, default='None')
	country = models.CharField(max_length=50, default='None')
	click = models.PositiveIntegerField(null=True,blank=True,default=0)

	def __str__(self):
		return f"{self.ip} is in device {self.device} on {self.date}"

	class Meta:
		ordering = ['-date']