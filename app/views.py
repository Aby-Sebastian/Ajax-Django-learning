from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from . models import Customer, Ip_address, Link_only_ip_address
from .forms import CreateCustomLinkForm
from django.http import JsonResponse
from django.utils import timezone
import uuid
import requests
from bs4 import BeautifulSoup
import geoip2.database
from device_detector import DeviceDetector




def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip
	
def links(request):
	ip = get_client_ip(request)
	a=Ip_address(ip=ip)
	a.save()
	all_ips = Ip_address.objects.all()
	links = Customer.objects.all().order_by('-id')
	form = CreateCustomLinkForm()
	context = {'links':links, 'form':form, 'all_ip':all_ips, 'ip':ip}
	return render(request, 'dashboard/links.html',context)

def scrape_title(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text,'html.parser')

	# print(res)
	return soup.title.string


def save_data(request):
	if request.method == 'POST':
		lid = request.POST.get('sid')
		if lid == '':
			form = CreateCustomLinkForm(request.POST)
		else:
			sid = Customer.objects.get(pk=lid)
			form = CreateCustomLinkForm(request.POST, instance=sid)

		uid = str(uuid.uuid4())[:5]
		# print("here-----------------",lid)

		short_url = request.POST['short_url']
		if short_url == '':
			short_url = uid
		print(form.errors)
		if form.is_valid():
			lid = request.POST.get('sid')
			value=request.POST['url']
			print(lid,value,short_url,sep=" ")
			print("----------------------Start--------------------------")
			# title = scrape_title(value)
			
			
			expiration = timezone.now() + timezone.timedelta(days=30)
			if lid == '':
				print('yes')
				custom_url = Customer(url=value,short_url=short_url)
			else:
				print('no')

				custom_url = Customer(id=lid,url=value,short_url=short_url)
			custom_url.save()
			cust = Customer.objects.values().order_by('-id')
			# print(cust)
			customer_values = list(cust)
			return JsonResponse({'status': 'save', 'customer_values':customer_values})
		else:
			return JsonResponse({'status': 0})


def delete(request):
	if request.method == 'POST':
		id = request.POST.get('sid')
		url=Customer.objects.get(pk=id)
		url.delete()
		return JsonResponse({'status':1, 'id':id})
	return JsonResponse({'status':0})

def edit_links(request):
	if request.method == 'POST':
		id = request.POST.get('sid')
		print(id)
		link = Customer.objects.get(pk=id)
		link_data = {'id':link.id, 'url':link.url, 'short_url':link.short_url}
		return JsonResponse(link_data)

def get_country_from_IP(ip_address):
	reader = geoip2.database.Reader('./GeoLite2-Country/GeoLite2-Country.mmdb')
	try:
		response = reader.country(ip_address)
		country_name = response.country.name

	except geoip2.errors.AddressNotFoundError:
		print("Its localhost you idiot")
		country_name = 'India'

	reader.close()
	return country_name

# def get_device(request):
# 	device = request.META['User-Agent']
# 	return device

def pages(request,pk):
	"""creates each page from links"""
	ua = request.headers.get('User-Agent')
	print(ua)
	# Parse UA string and load data to dict of 'os', 'client', 'device' keys
	device = DeviceDetector(ua).parse()
	link_ip = get_client_ip(request)
	country = get_country_from_IP(link_ip)
	print(country)
	page = Customer.objects.get(short_url=pk)
	b = Link_only_ip_address(ip=link_ip, url=page, country=country, device=device.os_name())
	b.save()

	# fetching for Chart data
	urls=Customer.objects.get(short_url=pk)
	all_urls = Link_only_ip_address.objects.filter(url=urls)
	country = Link_only_ip_address.objects.filter(url=urls)
	dat=[]
	labels=[]
	for i in country:
		dat.append(i.url)
		labels.append(i.date)
	# all_urls = Link_only_ip_address.objects.filter(url=urls)
	print(country)
	print(dat)
	print(labels)
	context={
		'page':page.url,
		'count':all_urls.count(),
		'url': urls,
		'data': all_urls,
		}
	return render(request, 'dashboard/page.html',context)

def data_for_page_Chart(request):
	return JsonResponse({
		'hi':'hiii'
		})