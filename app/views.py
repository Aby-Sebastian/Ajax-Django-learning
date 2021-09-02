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

# Variables
shortened_web_address = 'localhost:8000/page/'

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

# Parsing title from url
from urllib.request import urlopen
from lxml.html import parse

def title_parser(url):
    # url = "https://www.google.com"
    page = urlopen(url)
    p = parse(page)
    result = p.find(".//title").text
    return result

def links(request):
	ip = get_client_ip(request)
	a=Ip_address(ip=ip)
	a.save()
	all_ips = Ip_address.objects.all()
	links = Customer.objects.all().order_by('-id')
	all_urls = Link_only_ip_address.objects.all()
	form = CreateCustomLinkForm()

	# Chart data for all links
	days=Link_only_ip_address.objects.dates('date','day')
	names=[]
	dates=[]
	for i in range(len(days)):
	     s=Link_only_ip_address.objects.filter(date__date=days[i]).count()
	     names.append(s)
	     dates.append(days[i])

	context = {'links':links, 'form':form, 'all_ip':all_ips, 'ip':ip, 'labels':dates, 'data':names}
	return render(request, 'dashboard/links.html',context)

def scrape_title(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text,'html.parser')

	# print(res)
	return soup.title.string

def uid():
     uid = str(uuid.uuid4())[:5]
     return uid


def save_data(request):
	if request.method == 'POST':
		lid = request.POST.get('sid')
		if lid == '':
			form = CreateCustomLinkForm(request.POST)
		else:
			sid = Customer.objects.get(pk=lid)
			form = CreateCustomLinkForm(request.POST, instance=sid)

		#uid = str(uuid.uuid4())[:5]
		# print("here-----------------",lid)

		short_url = request.POST['short_url']
		if short_url == '':
			short_url = uid()
			if Customer.objects.filter(short_url=short_url).exists():
				short_url=uid()
		print(form.errors)
		if form.is_valid():
			lid = request.POST.get('sid')
			value=request.POST['url']
			print(lid,value,short_url,sep=" ")
			print("----------------------Start--------------------------")
			# title = scrape_title(value)
			
			
			expiration = timezone.now() + timezone.timedelta(days=30)
			title_data = title_parser(value)

			# QR code generator
		    # if request.method == "POST":
			# factory = qrcode.image.svg.SvgImage
			url_to_QR = f"localhost:8000/page/{short_url}"
			img = qrcode.make(url_to_QR)
			# stream = BytesIO()
			img.save(f"./media/QR_codes/{short_url}.png")

			# svg = stream.getvalue().decode()

			if lid == '':
				print('yes')
				custom_url = Customer(url=value,short_url=shortened_web_address+short_url, titles=title_data, qr_code=f"./QR_codes/{short_url}.png")
			else:
				print('no')

				custom_url = Customer(id=lid,url=value,short_url=shortened_web_address+short_url, titles=title_data, qr_code=f"./QR_codes/{short_url}.png")
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

'''
days=Link_only_ip_address.objects.dates('date','day')
Link_only_ip_address.objects.filter(date__date=days[0])
Link_only_ip_address.objects.filter(date__date=days[0]).count()
Link_only_ip_address.objects.filter(date__date=days.iterator).count()

'''
import qrcode
import qrcode.image.svg
from io import BytesIO

def pages(request,pk):
	"""creates each page from links"""
	ua = request.headers.get('User-Agent')
	# print(ua)
	# Parse UA string and load data to dict of 'os', 'client', 'device' keys
	device = DeviceDetector(ua).parse()
	link_ip = get_client_ip(request)
	country = get_country_from_IP(link_ip)
	print('pk is ',pk)
	page = Customer.objects.get(short_url=pk)

	

	# print(page.count)

	# saving user ip and details to models
	b = Link_only_ip_address(ip=link_ip, url=page, country=country, device=device.os_name(), click=page.total_clicks+1)
	b.url.increment_count()		# Increments url click count by 1
	b.url.save()				# saves b.url class
	b.save()					# saves b



	# fetching for Chart data
	urls=Customer.objects.get(short_url=pk)
	all_urls = Link_only_ip_address.objects.filter(url=urls)[:5]
	country = Link_only_ip_address.objects.filter(url=urls)
	dat=[]
	labels=[]
	for i in country:
		dat.append(i.url)
		labels.append(i.date)
	# all_urls = Link_only_ip_address.objects.filter(url=urls)
	# print(country)
	# print(dat)
	# print(labels)
	# New Chart data by date

	days=Link_only_ip_address.objects.dates('date','day')
	names=[]
	dates=[]
	for i in range(len(days)):
	     s=Link_only_ip_address.objects.filter(date__date=days[i], url=urls).count()
	     names.append(s)
	     dates.append(days[i])




	context={
		'page':page.url,
		'count':page.total_clicks,
		'title': page.titles,
		'url': urls,
		'data': all_urls,
		'names': names,
		'dates': dates,
		# 'svg': svg,
		'qr_code':page.qr_code
		}
	return render(request, 'dashboard/page.html',context)

def data_for_page_Chart(request):
	return JsonResponse({
		'hi':'hiii'
		})