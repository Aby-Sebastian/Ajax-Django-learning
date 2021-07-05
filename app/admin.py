from django.contrib import admin
from .models import Customer, Ip_address, Link_only_ip_address

# Register your models here.

admin.site.register(Customer)
admin.site.register(Ip_address)
admin.site.register(Link_only_ip_address)
