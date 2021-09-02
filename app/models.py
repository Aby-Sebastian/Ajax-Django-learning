from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
class Customer(models.Model):
	# created = models.DateTimeField(auto_now=True)
	# last_updated = models.DateTimeField(auto_now_add=True)
	url = models.CharField(max_length=150)
	short_url = models.CharField(max_length=20, unique=True)
	total_clicks = models.IntegerField(default=0, blank=True, null=True)
	titles = models.CharField(max_length=200,default="No title found", blank=True, null=True)
	qr_code = models.ImageField(upload_to='QR_codes',default='../static/images/young-man-avatar.jpg')
	

	def __str__(self):
		return self.short_url
	
	def increment_count(self):
		self.total_clicks+=1
		return self.total_clicks

	def save(self, *args, **kwargs):
		qrcode_img = qrcode.make(self.short_url)
		canvas = Image.new('RGB', (290,290), 'white')
		draw = ImageDraw.Draw(canvas)
		canvas.paste(qrcode_img)
		qrname = f"qr_code-{self.short_url}.png"
		buffer = BytesIO()
		canvas.save(buffer, 'PNG')
		self.qr_code.save(qrname, File(buffer), save=False)
		canvas.close()
		super().save(*args, **kwargs)


		
class Ip_address(models.Model):
    date = models.DateField(auto_now_add=True)
    ip = models.CharField(max_length=50)

    def __str__(self):
            return f"{self.ip} on {self.date}"

    class Meta:
    	ordering = ['-date']
                
class Countries(models.Model):
	country_name = models.CharField(max_length=50)

	def __str__(self):
		return self.country_name

class Devices(models.Model):
	device_name = models.CharField(max_length=50)

	def __str__(self):
		return self.device_name


class Link_only_ip_address(models.Model):
	url = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	ip = models.CharField(max_length=50)
	device = models.CharField(max_length=100, default='None')
	country = models.CharField(max_length=50, default='None')
	click = models.PositiveIntegerField(null=True,blank=True,default=0)
	# dev = models.ForeignKey(Devices, on_delete=models.CASCADE)
	# cou = models.ForeignKey(Countries, on_delete=models.CASCADE)
	# i_p = models.ForeignKey(Ip_address, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.ip} is in device {self.device} on {self.date}"

	class Meta:
		ordering = ['-date']